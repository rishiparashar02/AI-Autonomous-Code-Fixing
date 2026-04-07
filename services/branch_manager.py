import re
from git import Repo


def create_fix_branch(repo_path, bug_description):
    """Create or checkout a fix branch based on a bug description.

    Args:
        repo_path (str): Path to the Git repository.
        bug_description (str): Description of the bug.

    Returns:
        str: The name of the branch checked out.
    """
    # Convert description to a safe branch name
    normalized = bug_description.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    branch_name = f"ai-fix-{normalized}" if normalized else "ai-fix"

    repo = Repo(repo_path)

    # Checkout main branch if it exists
    try:
        repo.git.checkout("main")
    except Exception:
        pass

    # Checkout existing branch or create a new one
    if branch_name in repo.branches:
        repo.git.checkout(branch_name)
    else:
        repo.git.checkout("-b", branch_name)

    return branch_name
