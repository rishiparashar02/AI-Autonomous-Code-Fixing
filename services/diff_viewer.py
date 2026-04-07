from git import Repo


def show_git_diff(repo_path):
    """Show git diff between working tree and current branch.

    Args:
        repo_path (str): Path to the Git repository.

    Returns:
        str: The diff text.
    """
    repo = Repo(repo_path)

    # Git diff between working tree (including staged and unstaged) and HEAD
    diff_text = repo.git.diff('HEAD')

    # Print diff to terminal
    print(diff_text)

    return diff_text
