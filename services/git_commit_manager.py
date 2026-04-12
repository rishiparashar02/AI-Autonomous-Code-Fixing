from git import Repo


def commit_changes(repo_path, message):
    """Stage all changes and commit with the given message.

    Args:
        repo_path (str): Path to the Git repository.
        message (str): Commit message.

    Returns:
        bool: True if changes were committed, False if no changes were found.
    """
    repo = Repo(repo_path)
    repo.git.add("--all")
    if not repo.is_dirty(index=True, working_tree=True, untracked_files=True):
        return False
    repo.index.commit(message)
    return True


def push_branch(repo_path, branch_name):
    """Push the current branch to origin and set the upstream branch.

    Args:
        repo_path (str): Path to the Git repository.
        branch_name (str): The branch to push.

    Returns:
        str: A status message describing the push result.
    """
    repo = Repo(repo_path)
    try:
        repo.git.push("--set-upstream", "origin", branch_name)
        return f"Branch '{branch_name}' pushed to origin."
    except Exception as exc:
        return f"Failed to push branch '{branch_name}': {exc}"
