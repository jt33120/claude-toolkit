"""SessionStart hook: refresh CLAUDE.md after compaction, suggest bootstrap on a repo without one."""

import json
import os
import subprocess
import sys
from pathlib import Path

COMPACT = (
    "Context was just compacted. Before resuming, apply the dev:claude-md skill: from the corrections "
    "and decisions in this session's summary, update CLAUDE.md in place (80 lines max), then tell the "
    "user in one line what changed, or that nothing needed to."
)
BOOTSTRAP = "This repository has no CLAUDE.md. Offer /dev:bootstrap to the user once; do not run it unasked."
MISSING = "Plugin {0} is not enabled for this project: suggest `/plugin install {0}` or /dev:bootstrap."
REQUIRED = ("core@claude-toolkit",)


def is_git_repo(path):
    try:
        done = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=path,
                              capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return False
    return done.returncode == 0 and done.stdout.strip() == "true"


def enabled_plugins(project):
    enabled = {}
    for settings in (Path.home() / ".claude/settings.json", project / ".claude/settings.json",
                     project / ".claude/settings.local.json"):
        try:
            enabled.update(json.loads(settings.read_text(encoding="utf-8")).get("enabledPlugins") or {})
        except (OSError, ValueError, AttributeError):
            continue
    return {name for name, on in enabled.items() if on}


def messages(mode, project):
    if not is_git_repo(project):
        return []
    if mode == "compact":
        return [COMPACT]
    found = [] if (project / "CLAUDE.md").is_file() else [BOOTSTRAP]
    on = enabled_plugins(project)
    return found + [MISSING.format(name) for name in REQUIRED if name not in on]


def main(mode):
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        payload = {}
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())
    lines = messages(mode, project)
    if lines:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                                 "additionalContext": "\n".join(lines)}}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "startup"))
    except Exception:  # a hook must never break the session
        sys.exit(0)
