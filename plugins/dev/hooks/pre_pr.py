"""PreToolUse hook: block opening a PR/MR until /dev:audit diff has passed on the current HEAD."""

import json
import re
import subprocess
import sys
from pathlib import Path

OPENS_PR = re.compile(r"\b(?:gh\s+pr\s+create|glab\s+mr\s+create)\b")
MARKER = "claude-audit-ok"
BLOCK = (
    "Review required before opening a PR: run /dev:audit diff on this branch first. It records the "
    "pass for the current commit, then retry this command."
)


def git(cwd, *args):
    done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=5)
    return done.stdout.strip() if done.returncode == 0 else None


def allowed(payload):
    if payload.get("tool_name") not in {"Bash", "PowerShell"}:
        return True
    command = (payload.get("tool_input") or {}).get("command") or ""
    if not OPENS_PR.search(command):
        return True
    cwd = payload.get("cwd") or "."
    head, git_dir = git(cwd, "rev-parse", "HEAD"), git(cwd, "rev-parse", "--git-dir")
    if not head or not git_dir:
        return True
    marker = Path(cwd, git_dir, MARKER)
    return marker.is_file() and marker.read_text(encoding="utf-8").strip() == head


def main():
    payload = json.loads(sys.stdin.read() or "{}")
    if allowed(payload):
        return 0
    print(BLOCK, file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # never block the user because the hook itself failed
        sys.exit(0)
