# AI Autonomous Bug Fixing System

An intelligent system that analyzes GitHub repositories to locate and extract code snippets related to bug descriptions.

## Project Structure

```
ai-bug-fixer/
├── .venv/                     # Python virtual environment
├── cloned_repos/              # Temporary cloned repositories
├── main.py                    # CLI entry point
├── services/
│   ├── repo_manager.py        # Repository cloning and management
│   ├── file_scanner.py        # Source file scanning
│   ├── bug_locator.py         # Bug-related file identification
│   └── snippet_extractor.py   # Code snippet extraction
├── utils/
│   └── logger.py              # Logging utilities
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.x
- Git installed on your system

## Installation

1. Clone this repository or navigate to the project directory
2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the system using the command line interface:

```bash
python main.py <repo_url> "<bug_description>" [--dest <destination>]
```

### Arguments

- `repo_url`: GitHub repository URL (e.g., "https://github.com/microsoft/vscode.git")
- `bug_description`: Description of the bug to analyze (in quotes)
- `--dest`: Optional destination directory for cloned repos (default: "./cloned_repos")

### Example

```bash
python main.py https://github.com/octocat/Hello-World.git "function not working properly"
```

## Pipeline

The system follows a 4-step pipeline:

1. **Repository Cloning**: Clones the GitHub repository if not already present
2. **File Scanning**: Identifies all source code files (.py, .js, .java)
3. **Bug Location**: Finds files containing keywords from the bug description
4. **Snippet Extraction**: Extracts code snippets around matching lines

## Output

The system provides:
- Count of source files found
- Count of relevant files identified
- Count of code snippets extracted
- Detailed code snippets with file paths and line numbers

## Troubleshooting

- **Git not installed**: Ensure Git is available in your PATH
- **Permission denied**: Check write permissions for the destination directory
- **No snippets found**: Try different keywords or check if the repository contains the expected file types
- **Invalid URL**: Verify the repository URL is correct and accessible.
- **Network issues**: Check your internet connection if cloning fails.
- **GitPython errors**: Ensure GitPython is properly installed via `pip install gitpython`.

## Dependencies

- GitPython: A Python library used to interact with Git repositories.