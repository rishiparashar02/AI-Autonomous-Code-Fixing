#!/usr/bin/env python3
"""
Finalize AI Bug Fix - Test, Commit, and Push Script

This script assumes the AI fixes have been applied to a local repository branch.
It runs tests, commits changes if tests pass, and pushes the branch to origin.

Usage:
    python finalize_fix.py <repo_path> <branch_name> <bug_description>

Arguments:
    repo_path: Path to the local Git repository
    branch_name: Name of the branch with applied fixes
    bug_description: Description of the bug (used for commit message)
"""

import os
import sys
import subprocess
from services.test_runner import run_tests
from services.git_commit_manager import commit_changes, push_branch
from services.fix_summary import create_fix_summary_file


def main():
    if len(sys.argv) != 4:
        print("Usage: python finalize_fix.py <repo_path> <branch_name> <bug_description>")
        sys.exit(1)

    repo_path = sys.argv[1]
    branch_name = sys.argv[2]
    bug_description = sys.argv[3]

    if not os.path.exists(repo_path):
        print(f"Error: Repository path {repo_path} does not exist")
        sys.exit(1)

    # Change to repo directory
    os.chdir(repo_path)

    # Check if we're on the correct branch
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()
        if current_branch != branch_name:
            print(f"Warning: Currently on branch '{current_branch}', expected '{branch_name}'")
            # Switch to the branch
            subprocess.run(['git', 'checkout', branch_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error checking/switching branch: {e}")
        sys.exit(1)

    # Run tests
    print("Running tests...")
    test_results = run_tests(repo_path)
    print(f"Test status: {test_results['status']}")

    if test_results['status'] not in ('passed', 'skipped'):
        print(f"Tests failed or errored. Status: {test_results['status']}")
        print(f"Summary: {test_results['summary']}")
        print("Not committing or pushing changes.")
        sys.exit(1)

    # Get changed files
    try:
        result = subprocess.run(['git', 'diff', '--name-only', 'HEAD'], capture_output=True, text=True, check=True)
        changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        changed_files = []

    # Create summary file
    if changed_files:
        summary_file = create_fix_summary_file(repo_path, branch_name, bug_description, changed_files)
        print(f"Created summary file: {summary_file}")

    # Commit changes
    commit_message = f"AI fix branch {branch_name}: {bug_description}"
    print(f"Committing changes with message: {commit_message}")
    committed = commit_changes(repo_path, commit_message)
    if not committed:
        print("No changes to commit.")
        sys.exit(0)

    # Push branch
    print(f"Pushing branch {branch_name} to origin...")
    push_status = push_branch(repo_path, branch_name)
    print(f"Push status: {push_status}")

    print("Fix finalization complete!")


if __name__ == "__main__":
    main()