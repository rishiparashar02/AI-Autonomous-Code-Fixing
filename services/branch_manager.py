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
    # Extract key words from description (skip common filler)
    common_words = {'the', 'is', 'are', 'a', 'an', 'and', 'or', 'if', 'bug', 'bugs', 'fix', 'fixes', 'error', 'issue', 'please', 'check', 'any', 'more', 'changes', 'needed', 'everything', 'correct', 'already', 'you', 'just'}
    words = re.findall(r'\b[a-z]+\b', bug_description.lower())
    key_words = [w for w in words if w not in common_words][:2]  # Take first 2 significant words
    
    if key_words:
        normalized = '-'.join(key_words)
    else:
        normalized = "issue"
    
    branch_name = f"ai-fix-{normalized}"

    repo = Repo(repo_path)

    # Checkout main branch if it exists
    try:
        repo.git.checkout("main")
    except Exception:
        pass

    # Checkout existing branch or create a new one
    existing_branches = {branch.name for branch in repo.branches}
    if branch_name in existing_branches:
        repo.git.checkout(branch_name)
    else:
        repo.git.checkout("-b", branch_name)

    return branch_name
