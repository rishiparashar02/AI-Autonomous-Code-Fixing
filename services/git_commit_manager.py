from git import Repo


def commit_changes(repo_path, message):
    """Stage all changes and commit with the given message.

    Args:
        repo_path (str): Path to the Git repository.
        message (str): Commit message.
    """
    repo = Repo(repo_path)
    repo.git.add("--all")
    repo.index.commit(message)
    return message
