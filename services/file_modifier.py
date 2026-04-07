def apply_fix_to_file(file_path, new_code):
    """Apply a fix to a file by replacing its contents with new code.

    Args:
        file_path (str): Path to the file to update.
        new_code (str): The new code that should replace the existing content.
    """
    # Write the new code to the file (overwrites existing content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_code)


def apply_ai_fix(file_path, fixed_code):
    """Apply an AI-generated fix by replacing the buggy section in a file.

    This implementation overwrites the file with the provided fixed code.
    It assumes that the AI-generated `fixed_code` represents the updated
    version of the file or the corrected snippet meant to replace the file.

    Args:
        file_path (str): Path to the file to update.
        fixed_code (str): The AI-generated fixed code.

    Returns:
        str: The path to the updated file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(fixed_code)
    return file_path
