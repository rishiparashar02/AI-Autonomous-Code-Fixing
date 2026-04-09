from pathlib import Path

from main import analyze_bug
from services.bug_locator import find_relevant_files
from services.snippet_extractor import extract_snippets


def test_find_relevant_files_falls_back_when_no_keyword_overlap(tmp_path):
    file_a = tmp_path / "main.py"
    file_b = tmp_path / "math_utils.py"
    file_a.write_text("print('hello')\n", encoding="utf-8")
    file_b.write_text("def divide(a, b):\n    return a / 0\n", encoding="utf-8")

    files = [str(file_a), str(file_b)]
    relevant = find_relevant_files(files, "Fix runtime errors and incorrect method usage")

    assert relevant == files


def test_extract_snippets_has_fallback_when_no_keyword_match(tmp_path):
    target = tmp_path / "string_utils.py"
    target.write_text("def reverse_string(s):\n    return s.revers()\n", encoding="utf-8")

    result = extract_snippets(str(target), {"runtime", "error"})

    assert str(target) in result
    assert len(result[str(target)]) == 1
    assert result[str(target)][0]["line"] == 1
    assert "reverse_string" in result[str(target)][0]["snippet"]


def test_analyze_bug_returns_locations_with_generic_bug_text(tmp_path, monkeypatch):
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    (repo_path / "main.py").write_text("from math_utils import divide\nprint(divide(10,2))\n", encoding="utf-8")
    (repo_path / "math_utils.py").write_text("def divide(a, b):\n    return a / 0\n", encoding="utf-8")
    (repo_path / "string_utils.py").write_text("def reverse_string(s):\n    return s.revers()\n", encoding="utf-8")

    source_files = sorted(str(path) for path in Path(repo_path).glob("*.py"))

    monkeypatch.setattr("main.clone_repository", lambda repo_url, destination_folder: str(repo_path))
    monkeypatch.setattr("main.scan_source_files", lambda repo: source_files)
    monkeypatch.setattr("main.generate_patch", lambda bug, snippet: "# patched\n" + snippet)
    monkeypatch.setattr("main.generate_diff_patch", lambda before, after, file_path: f"diff for {file_path}")
    monkeypatch.setattr("main.save_patch_to_file", lambda patch, index: None)

    result = analyze_bug(
        repo_url="https://github.com/rishiparashar02/ai-bug-test-repo",
        bug_description="Fix runtime errors and incorrect method usage",
        dest=str(tmp_path / "cloned_repos"),
        max_locations=5,
        apply_fixes=False,
    )

    assert result is not None
    assert result["files_scanned"] == 3
    assert len(result["relevant_files"]) >= 1
    assert len(result["suggested_fixes"]) >= 1
    assert all(fix["file"] for fix in result["suggested_fixes"])
    assert all(fix["original_code"] for fix in result["suggested_fixes"])
