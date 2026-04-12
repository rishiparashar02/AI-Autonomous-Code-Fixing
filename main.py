#!/usr/bin/env python3
"""
AI Bug Fixer - Entry point for the autonomous bug fixing system.
"""

import argparse
import os
from services.repo_manager import clone_repository
from services.file_scanner import scan_source_files
from services.bug_locator import find_relevant_files, bug_description_keywords
from services.snippet_extractor import extract_snippets
from services.ai_patch_generator import generate_patch
from services.branch_manager import create_fix_branch
from services.file_modifier import apply_ai_fix
from services.patch_generator import generate_patch as generate_diff_patch, save_patch_to_file
from services.diff_viewer import show_git_diff
from services.git_commit_manager import commit_changes, push_branch
from services.fix_summary import create_fix_summary_file
from services.test_runner import run_tests
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

    keywords = bug_description_keywords(bug_description)
    snippets = {}
    for file_path in relevant_files:
        file_snippets = extract_snippets(file_path, keywords)
        snippets.update(file_snippets)

    all_snippets = []
    for file_path, file_snips in snippets.items():
        for snip in file_snips:
            all_snippets.append((file_path, snip))
    all_snippets = all_snippets[:max_locations]

    fix_branch_name = None
    if apply_fixes and all_snippets:
        fix_branch_name = create_fix_branch(repo_path, bug_description)

    suggested_fixes = []
    changed_files = set()
    overall_diff = None

    for i, (file_path, snip) in enumerate(all_snippets, 1):
        suggested_fix = generate_patch(bug_description, snip['snippet'])
        patch = None
        diff_text = None
        fix_applied = False
        if suggested_fix:
            patch = generate_diff_patch(snip['snippet'], suggested_fix, file_path)
            save_patch_to_file(patch, i)

            if apply_fixes:
                _, fix_applied = apply_ai_fix(file_path, snip['snippet'], suggested_fix)
                if fix_applied:
                    changed_files.add(file_path)
                    overall_diff = show_git_diff(repo_path)
                    diff_text = overall_diff

        suggested_fixes.append({
            "file": file_path,
            "line": snip['line'],
            "original_code": snip['snippet'],
            "suggested_fix": suggested_fix,
            "patch": patch,
            "branch": fix_branch_name,
            "fix_applied": fix_applied,
            "diff": diff_text,
        })

    test_results = None
    push_status = None
    fix_summary_file = None

    if apply_fixes:
        test_results = run_tests(repo_path)
        if changed_files:
            fix_summary_file = create_fix_summary_file(
                repo_path,
                fix_branch_name,
                bug_description,
                sorted(changed_files),
            )
            commit_message = f"AI fix branch {fix_branch_name}: {bug_description}"
            committed = commit_changes(repo_path, commit_message)
            if committed:
                if test_results["status"] in ("passed", "skipped"):
                    push_status = push_branch(repo_path, fix_branch_name)
                else:
                    push_status = (
                        f"Changes committed locally, but push skipped because tests status is '{test_results['status']}'."
                    )
            else:
                push_status = "No file changes were committed."
        else:
            push_status = "No file changes were detected; nothing committed or pushed."

    return {
        "repo": repo_url,
        "bug": bug_description,
        "repo_path": repo_path,
        "fix_branch": fix_branch_name,
        "apply_fixes": apply_fixes,
        "files_scanned": len(source_files),
        "relevant_files": relevant_files,
        "suggested_fixes": suggested_fixes,
        "test_results": test_results,
        "push_status": push_status,
        "fix_summary_file": fix_summary_file,
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
    if result.get("fix_branch"):
        print(f"Fix branch: {result['fix_branch']}")
    if result.get("test_results"):
        print(f"Test status: {result['test_results']['status']}")
    if result.get("push_status"):
        print(f"Push status: {result['push_status']}")
    if result.get("fix_summary_file"):
        print(f"Branch summary file: {result['fix_summary_file']}")
        print(f"To finalize and push manually, run: python finalize_fix.py \"{result['repo_path']}\" \"{result['fix_branch']}\" \"{result['bug']}\"")

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