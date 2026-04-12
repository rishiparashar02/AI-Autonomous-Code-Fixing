# AI Autonomous Bug Fixing System

An intelligent system that analyzes GitHub repositories to locate and extract code snippets related to bug descriptions.

## Project Structure

```
ai-bug-fixer/
├── .venv/                     # Python virtual environment
├── cloned_repos/              # Temporary cloned repositories
├── main.py                    # CLI entry point for analysis
├── finalize_fix.py            # Script to test, commit, and push fixes
├── services/
│   ├── repo_manager.py        # Repository cloning and management
│   ├── file_scanner.py        # Source file scanning
│   ├── bug_locator.py         # Bug-related file identification
│   ├── snippet_extractor.py   # Code snippet extraction
│   ├── ai_patch_generator.py  # AI-powered patch generation
│   ├── branch_manager.py      # Git branch management
│   ├── file_modifier.py       # File modification utilities
│   ├── patch_generator.py     # Patch file generation
│   ├── diff_viewer.py         # Git diff display
│   ├── git_commit_manager.py  # Git commit and push operations
│   ├── fix_summary.py         # Branch summary generation
│   └── test_runner.py         # Test execution utilities
├── utils/
│   └── logger.py              # Logging utilities
├── tests/                     # Unit tests
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

## Finalize Fix Script

After running the main analysis and applying fixes, use the finalize script to test, commit, and push:

```bash
python finalize_fix.py <repo_path> <branch_name> "<bug_description>"
```

This script will:
- Run repository tests
- If tests pass, commit changes and push to the new branch
- Create a summary README in the branch

### Arguments

- `repo_path`: Path to the cloned repository (e.g., "./cloned_repos/repo-name")
- `branch_name`: The AI-generated branch name (shown in analysis output)
- `bug_description`: The same bug description used in analysis

### Example

```bash
python finalize_fix.py ./cloned_repos/my-repo ai-fix-divide-by-zero "fix divide by zero error"
```

## Branch and fix behavior

When fixes are applied, the system will:
- create a new branch in the cloned repository based on the bug description
- write the AI changes into the source files on that branch
- generate a branch summary README file listing the changed files
- run repository tests if a test suite is detected
- commit the changes locally and push the branch to origin if possible

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