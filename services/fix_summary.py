import os
import re


def sanitize_filename(name):
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", name)


def create_fix_summary_file(repo_path, branch_name, bug_description, changed_files):
    """Write a branch-specific summary README for the fix branch.

    Args:
        repo_path (str): Local repository path.
        branch_name (str): The branch name.
        bug_description (str): Bug description from the user.
        changed_files (list[str]): Paths of files changed in the fix.

    Returns:
        str: Path to the created summary file.
    """
    summary_filename = f"AI_FIX_SUMMARY_{sanitize_filename(branch_name)}.md"
    summary_path = os.path.join(repo_path, summary_filename)
    lines = [
        f"# AI Fix Summary for branch `{branch_name}`\n",
        f"**Bug description:** {bug_description}\n",
        "## Changed files\n",
    ]
    if changed_files:
        for file_path in changed_files:
            lines.append(f"- `{os.path.relpath(file_path, repo_path)}`\n")
    else:
        lines.append("- No file changes were detected.\n")

    lines.extend(
        [
            "\n## Notes\n",
            "This branch was created by the AI Autonomous Bug Fixing System.\n",
            "Review the generated patch/diff and push this branch when ready.\n",
        ]
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return summary_path
