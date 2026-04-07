import os

def scan_source_files(repo_path):
    """
    Scans all files in the cloned repository and returns a list of source code files.
    
    Args:
        repo_path (str): The path to the cloned repository.
    
    Returns:
        list: A list of absolute paths to source code files (.py, .js, .ts, .java, .go, .cpp).
    
    Ignores directories: tests, test, __pycache__, .git, .venv, docs, and hidden directories.
    """
    source_files = []
    extensions = ['.py', '.js', '.ts', '.java', '.go', '.cpp']
    for root, dirs, files in os.walk(repo_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', '.venv', 'env', '.env', '__pycache__', 'node_modules', 'tests', 'test', '.git', 'docs']]
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                source_files.append(os.path.join(root, file))
    return source_files