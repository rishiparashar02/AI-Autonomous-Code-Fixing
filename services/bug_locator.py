def find_relevant_files(files, bug_description):
    """
    Finds relevant files based on keywords from the bug description.
    
    Args:
        files (list): A list of file paths to search in.
        bug_description (str): A description of the bug.
    
    Returns:
        list: A list of file paths that contain matching keywords.
    """
    # Extract keywords: split by space, convert to lowercase, remove short words
    keywords = set(word.lower() for word in bug_description.split() if len(word) > 2)
    
    relevant_files = []
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                if any(keyword in content for keyword in keywords):
                    relevant_files.append(file_path)
        except:
            # Skip files that can't be read
            pass
    
    return relevant_files