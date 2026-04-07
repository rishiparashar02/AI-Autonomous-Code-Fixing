import os
from git import Repo

def clone_repository(repo_url, destination_folder):
    """
    Clones a GitHub repository to a local folder using GitPython.
    
    Args:
        repo_url (str): The URL of the GitHub repository to clone.
        destination_folder (str): The local path where the repository should be cloned.
    
    Returns:
        str: The local path of the repository.
    
    If the repository already exists locally, it skips cloning.
    """
    if os.path.exists(destination_folder):
        print(f"Repository already exists at {destination_folder}. Skipping clone.")
        return destination_folder
    
    try:
        Repo.clone_from(repo_url, destination_folder)
        print(f"Successfully cloned {repo_url} to {destination_folder}")
        return destination_folder
    except Exception as e:
        print(f"Error cloning repository: {e}")
        return None