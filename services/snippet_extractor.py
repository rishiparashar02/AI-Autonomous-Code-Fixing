def extract_snippets(file_path, keywords, fallback_if_empty=True):
    """
    Extracts code snippets around lines containing specified keywords in a file.
    
    Args:
        file_path (str): The path to the file to analyze.
        keywords (list or set): A list or set of keywords to search for.
    
    Returns:
        dict: A dictionary with file_path as key and list of snippet dictionaries as value.
              Each snippet dict contains 'line' (1-based) and 'snippet' (21 lines of code).
              Limited to maximum 3 snippets per file.
    """
    snippets = []
    lines_seen = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            line_num = i + 1
            if line_num not in lines_seen and any(keyword.lower() in line.lower() for keyword in keywords):
                # Extract snippet: 10 lines before and 10 lines after (total 21 lines)
                start = max(0, i - 10)
                end = min(len(lines), i + 11)
                snippet = ''.join(lines[start:end])
                snippets.append({
                    'line': line_num,
                    'snippet': snippet
                })
                lines_seen.add(line_num)
                
                # Limit to 3 snippets per file
                if len(snippets) >= 3:
                    break
        if not snippets and fallback_if_empty and lines:
            end = min(len(lines), 21)
            snippets.append({
                'line': 1,
                'snippet': ''.join(lines[0:end])
            })
    except:
        # Skip files that can't be read
        pass
    
    return {file_path: snippets}