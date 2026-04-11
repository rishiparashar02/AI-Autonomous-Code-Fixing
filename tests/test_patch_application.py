"""Tests for applying AI/snippet replacements to files and analyze_bug(apply_fixes=True)."""

import shutil
import subprocess

import pytest

from main import analyze_bug
from services.file_modifier import (
    _replace_first_snippet_occurrence,
    apply_ai_fix,
    apply_fix_to_file,
)
from services.branch_manager import create_fix_branch


def test_replace_first_snippet_exact_match():
    content = "aaa\nORIGINAL\nbbb\n"
    updated, ok = _replace_first_snippet_occurrence(content, "ORIGINAL", "FIXED")
    assert ok
    assert "FIXED" in updated
    assert "ORIGINAL" not in updated


def test_replace_first_snippet_crlf_content_lf_snippet():
    existing = "line1\r\nORIGINAL\r\nline2\r\n"
    updated, ok = _replace_first_snippet_occurrence(existing, "ORIGINAL\n", "FIXED\n")
    assert ok
    assert "FIXED" in updated


def test_replace_first_snippet_not_found():
    content = "no match here\n"
    updated, ok = _replace_first_snippet_occurrence(content, "X", "Y")
    assert not ok
    assert updated == content


def test_apply_ai_fix_writes_file(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("def foo():\n    return 1\n", encoding="utf-8")
    _, ok = apply_ai_fix(str(f), "return 1\n", "return 2\n")
    assert ok
    assert "return 2" in f.read_text(encoding="utf-8")


def test_apply_fix_to_file_overwrites(tmp_path):
    f = tmp_path / "b.py"
    f.write_text("old", encoding="utf-8")
    apply_fix_to_file(str(f), "new")
    assert f.read_text(encoding="utf-8") == "new"


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_create_fix_branch_creates_named_branch(tmp_path):
    repo = tmp_path / "g"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "t@t.com"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "t"],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    (repo / "README.md").write_text("# x\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=repo,
        check=True,
        capture_output=True,
    )

    name = create_fix_branch(str(repo), "Fix divide by zero")
    assert name.startswith("ai-fix-")
    # Branch exists
    out = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    assert out.stdout.strip() == name


def test_analyze_bug_apply_fixes_updates_repo_files(tmp_path, monkeypatch):
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    math_py = repo_path / "math_utils.py"
    math_py.write_text("def divide(a, b):\n    return a / 0\n", encoding="utf-8")

    def fake_clone(url, destination_folder):
        return str(repo_path)

    monkeypatch.setattr("main.clone_repository", fake_clone)
    monkeypatch.setattr(
        "main.generate_patch",
        lambda bug, snip: "def divide(a, b):\n    return (a / b) if b else 0\n",
    )
    monkeypatch.setattr(
        "main.generate_diff_patch",
        lambda before, after, fp: "unified diff",
    )
    monkeypatch.setattr("main.save_patch_to_file", lambda patch, index: None)
    monkeypatch.setattr("main.create_fix_branch", lambda rp, bug: "ai-fix-test-branch")
    monkeypatch.setattr("main.show_git_diff", lambda rp: "git-diff-stub")

    result = analyze_bug(
        repo_url="https://github.com/example/test.git",
        bug_description="fix divide by zero error",
        dest=str(tmp_path / "cloned_repos"),
        max_locations=5,
        apply_fixes=True,
    )

    assert result is not None
    assert result["repo_path"] == str(repo_path)
    assert result["fix_branch"] == "ai-fix-test-branch"
    assert len(result["suggested_fixes"]) >= 1
    fix0 = result["suggested_fixes"][0]
    assert fix0["fix_applied"] is True
    assert "if b" in math_py.read_text(encoding="utf-8")
