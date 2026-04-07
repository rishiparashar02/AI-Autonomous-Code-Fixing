#!/usr/bin/env python3
"""
AI Bug Fixer - Entry point for the autonomous bug fixing system.
"""

import argparse
import os
from services.repo_manager import clone_repository
from services.file_scanner import scan_source_files
from services.bug_locator import find_relevant_files
from services.snippet_extractor import extract_snippets
from services.ai_patch_generator import generate_patch
from services.branch_manager import create_fix_branch
from services.file_modifier import apply_ai_fix
from services.patch_generator import generate_patch as generate_diff_patch, save_patch_to_file
from services.diff_viewer import show_git_diff
from utils.logger import setup_logger

logger = setup_logger(__name__)


def analyze_bug(repo_url, bug_description, dest="./cloned_repos", max_locations=5, apply_fixes=False):
    """Analyze a repository for a bug and optionally apply fixes.

    Args:
        repo_url (str): GitHub repository URL.
        bug_description (str): Bug description.
        dest (str): Destination directory for cloned repo.
        max_locations (int): Maximum bug locations to process.
        apply_fixes (bool): Whether to create a branch and apply fixes.

    Returns:
        dict: Analysis results.
    """
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    dest_path = os.path.join(dest, repo_name)

    logger.info(f"Starting bug fixing process for {repo_url}")

    repo_path = clone_repository(repo_url, dest_path)
    if not repo_path:
        logger.error("Failed to clone repository.")
        return None

    source_files = scan_source_files(repo_path)
    relevant_files = find_relevant_files(source_files, bug_description)

    keywords = set(word.lower() for word in bug_description.split() if len(word) > 2)
    snippets = {}
    for file_path in relevant_files:
        file_snippets = extract_snippets(file_path, keywords)
        snippets.update(file_snippets)

    all_snippets = []
    for file_path, file_snips in snippets.items():
        for snip in file_snips:
            all_snippets.append((file_path, snip))
    all_snippets = all_snippets[:max_locations]

    suggested_fixes = []
    for i, (file_path, snip) in enumerate(all_snippets, 1):
        suggested_fix = generate_patch(bug_description, snip['snippet'])
        patch = None
        diff_text = None
        branch_name = None
        if suggested_fix:
            patch = generate_diff_patch(snip['snippet'], suggested_fix, file_path)
            save_patch_to_file(patch, i)

            if apply_fixes:
                branch_name = create_fix_branch(repo_path, bug_description)
                apply_ai_fix(file_path, suggested_fix)
                diff_text = show_git_diff(repo_path)

        suggested_fixes.append({
            "file": file_path,
            "line": snip['line'],
            "original_code": snip['snippet'],
            "suggested_fix": suggested_fix,
            "patch": patch,
            "branch": branch_name,
            "diff": diff_text,
        })

    return {
        "repo": repo_url,
        "bug": bug_description,
        "files_scanned": len(source_files),
        "relevant_files": relevant_files,
        "suggested_fixes": suggested_fixes,
    }


def main():
    parser = argparse.ArgumentParser(description="AI Autonomous Bug Fixing System")
    parser.add_argument("repo_url", help="GitHub repository URL to clone")
    parser.add_argument("bug_description", help="Description of the bug to locate")
    parser.add_argument("--dest", default="./cloned_repos", help="Destination directory for cloned repo")

    args = parser.parse_args()

    result = analyze_bug(args.repo_url, args.bug_description, dest=args.dest, apply_fixes=True)
    if not result:
        return

    # Print summary
    print("\n=== RESULTS ===")
    print(f"Repository: {result['repo']}")
    print(f"Bug Description: {result['bug']}")
    print(f"Source Files Found: {result['files_scanned']}")
    print(f"Relevant Files: {len(result['relevant_files'])}")
    print(f"Code Snippets: {len(result['suggested_fixes'])}")

    for i, fix in enumerate(result['suggested_fixes'], 1):
        print(f"\nBug Location {i}:")
        print(f"File: {fix['file']}")
        print(f"Line: {fix['line']}")
        print("Suggested Fix:")
        print(fix['suggested_fix'])
        print("--- Patch ---")
        print(fix['patch'])
        if fix['diff']:
            print("--- Git Diff After Fix ---")
            print(fix['diff'])
            print("AI fix applied in new branch. Please review the diff and commit manually if satisfied.")

if __name__ == "__main__":
    main()