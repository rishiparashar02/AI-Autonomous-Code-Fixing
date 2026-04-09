import re


def _tokenize(text):
    return {token for token in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]+", (text or "").lower()) if len(token) > 2}


def find_relevant_files(files, bug_description, fallback_limit=10):
    """
    Finds relevant files based on bug description keywords.

    If no keyword matches are found, it falls back to returning the first
    source files so downstream stages can still surface candidate locations.
    """
    keywords = _tokenize(bug_description)
    scored_files = []

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content_tokens = _tokenize(f.read())

            overlap = len(keywords.intersection(content_tokens))
            if overlap > 0:
                scored_files.append((overlap, file_path))
        except Exception:
            # Skip files that can't be read
            pass

    if scored_files:
        scored_files.sort(key=lambda item: item[0], reverse=True)
        return [file_path for _, file_path in scored_files]

    return files[: max(0, fallback_limit)]