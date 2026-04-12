import os
import subprocess
import sys


def has_tests(repo_path):
    if os.path.isdir(os.path.join(repo_path, "tests")):
        return True
    if os.path.exists(os.path.join(repo_path, "pytest.ini")):
        return True
    if os.path.exists(os.path.join(repo_path, "pyproject.toml")):
        try:
            with open(os.path.join(repo_path, "pyproject.toml"), "r", encoding="utf-8") as f:
                return "[tool.pytest.ini_options]" in f.read() or "pytest" in f.read()
        except OSError:
            return False
    return False


def run_tests(repo_path, timeout=300):
    """Try to execute repository tests and return summary information.

    Args:
        repo_path (str): Local repository path.
        timeout (int): Test execution timeout in seconds.

    Returns:
        dict: Test execution results and output.
    """
    if not has_tests(repo_path):
        return {
            "status": "skipped",
            "summary": "No test configuration detected in the repository.",
            "returncode": None,
            "stdout": "",
            "stderr": "",
        }

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        summary = "passed" if result.returncode == 0 else "failed"
        return {
            "status": summary,
            "summary": result.stdout.strip() or result.stderr.strip(),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except FileNotFoundError as exc:
        return {
            "status": "error",
            "summary": f"Pytest not found: {exc}",
            "returncode": None,
            "stdout": "",
            "stderr": str(exc),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "summary": "Test execution timed out.",
            "returncode": None,
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
        }
