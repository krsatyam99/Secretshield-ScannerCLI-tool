import subprocess
from pathlib import Path
from git import Repo

def install_pre_commit_hook(repo_path: Path):
    """Write a pre-commit hook script to .git/hooks/pre-commit."""
    repo = Repo(repo_path)
    hook_path = Path(repo.git_dir) / "hooks" / "pre-commit"
    
    hook_script = """#!/bin/bash
# SecretShield pre-commit hook — blocks commits with exposed secrets

# Run scan on staged files
python main.py scan --staged
if [ $? -ne0 ]; then
    echo "Secrets detected. Commit blocked. Run 'python main.py scan .' to review."
    exit 1
fi
exit 0
"""
    
    hook_path.parent.mkdir(parents=True, exist_ok=True)
    # ADDED encoding="utf-8" HERE TO FIX THE UNICODE ERROR
    hook_path.write_text(hook_script, encoding="utf-8")
    
    try:
        import os
        import stat
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
    except Exception as e:
        print(f"Warning: Could not set executable permissions: {e}")
        
    print(f"✅ Pre-commit hook installed at {hook_path}")

def get_staged_files(repo_path: Path) -> list[Path]:
    """Get list of files staged in git (ready to commit)."""
    repo = Repo(repo_path)
    staged_files = []
    # This specifically looks for changes in the index vs HEAD
    for diff in repo.index.diff("HEAD"):
        # We need the absolute path or the path relative to project root
        file_path = repo_path / diff.b_path
        if file_path.exists():
            staged_files.append(file_path)
    return staged_files