import difflib
import os


def generate_patch(original_code, fixed_code, file_path):
    """
    Generates a git-style unified diff patch between original and fixed code.
    
    Args:
        original_code (str): The original code snippet.
        fixed_code (str): The AI-suggested fixed code.
        file_path (str): The file path for the diff headers.
    
    Returns:
        str: The unified diff patch as a string.
    """
    # Split code into lines
    original_lines = original_code.splitlines(keepends=True)
    fixed_lines = fixed_code.splitlines(keepends=True)
    
    # Generate unified diff
    diff = difflib.unified_diff(
        original_lines,
        fixed_lines,
        fromfile=f"original/{file_path}",
        tofile=f"fixed/{file_path}",
        lineterm=''
    )
    
    # Join the diff lines into a single string
    return ''.join(diff)


def save_patch_to_file(patch_text, patch_index):
    """
    Saves a patch to a file in the generated_patches directory.
    
    Args:
        patch_text (str): The patch content to save.
        patch_index (int): The index number for the patch file name.
    
    Returns:
        str: The path to the saved patch file.
    """
    # Create directory if it doesn't exist
    patch_dir = "generated_patches"
    os.makedirs(patch_dir, exist_ok=True)
    
    # Generate file name
    file_name = f"patch_{patch_index}.diff"
    file_path = os.path.join(patch_dir, file_name)
    
    # Write patch to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(patch_text)

    return file_path