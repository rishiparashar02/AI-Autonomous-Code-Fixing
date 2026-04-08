def _replace_first_snippet_occurrence(file_content, original_snippet, fixed_snippet):
    """Replace the first exact occurrence of a snippet in file content."""
    if not original_snippet or not fixed_snippet:
        return file_content, False

    idx = file_content.find(original_snippet)
    if idx == -1:
        return file_content, False

    updated = file_content[:idx] + fixed_snippet + file_content[idx + len(original_snippet):]
    return updated, True


def apply_fix_to_file(file_path, new_code):
    """Apply a fix to a file by replacing its contents with new code.

    Args:
        file_path (str): Path to the file to update.
        new_code (str): The new full file content.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_code)


def apply_ai_fix(file_path, original_snippet, fixed_code):
    """Apply an AI-generated fix by replacing only the matched snippet.

    Args:
        file_path (str): Path to the file to update.
        original_snippet (str): Original extracted snippet.
        fixed_code (str): The AI-generated fixed code.

    Returns:
        tuple[str, bool]: The path and whether replacement was applied.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        existing_content = f.read()

    updated_content, replaced = _replace_first_snippet_occurrence(
        existing_content, original_snippet, fixed_code
    )

    if replaced:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

    return file_path, replaced
