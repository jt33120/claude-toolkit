"""Behaviour of the dev plugin hooks, fed with the JSON Claude Code sends on stdin."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1] / "plugins/dev/hooks"


def run(script, payload, *args, env=None):
    return subprocess.run([sys.executable, str(HOOKS / script), *args], input=json.dumps(payload),
                          capture_output=True, text=True, env=env, timeout=30)


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


class HookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "x")
        self.home = self.repo / "home"
        (self.home / ".claude").mkdir(parents=True)
        self.env = {**os.environ, "HOME": str(self.home), "USERPROFILE": str(self.home),
                    "CLAUDE_PROJECT_DIR": str(self.repo)}

    def tearDown(self):
        self.tmp.cleanup()

    def context(self, mode):
        out = run("session.py", {"cwd": str(self.repo)}, mode, env=self.env).stdout
        return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out.strip() else ""

    def enable_core(self):
        (self.repo / ".claude").mkdir(exist_ok=True)
        (self.repo / ".claude/settings.json").write_text(
            json.dumps({"enabledPlugins": {"core@claude-toolkit": True}}), encoding="utf-8")

    def test_compact_asks_for_claude_md_update(self):
        self.assertIn("dev:claude-md", self.context("compact"))

    def test_startup_is_silent_on_a_ready_repo(self):
        (self.repo / "CLAUDE.md").write_text("# CLAUDE.md\n", encoding="utf-8")
        self.enable_core()
        self.assertEqual(self.context("startup"), "")

    def test_startup_suggests_bootstrap_and_missing_plugin(self):
        text = self.context("startup")
        self.assertIn("/dev:bootstrap", text)
        self.assertIn("core@claude-toolkit", text)

    def test_nothing_outside_a_git_repo(self):
        with tempfile.TemporaryDirectory() as bare:
            env = {**self.env, "CLAUDE_PROJECT_DIR": bare}
            out = run("session.py", {"cwd": bare}, "compact", env=env).stdout
        self.assertEqual(out.strip(), "")

    def pr(self, command, tool="Bash"):
        payload = {"tool_name": tool, "tool_input": {"command": command}, "cwd": str(self.repo)}
        return run("pre_pr.py", payload).returncode

    def test_pr_blocked_until_audit_marker_matches_head(self):
        self.assertEqual(self.pr("gh pr create --fill"), 2)
        self.assertEqual(self.pr("glab mr create", tool="PowerShell"), 2)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.repo, capture_output=True,
                              text=True).stdout.strip()
        (self.repo / ".git/claude-audit-ok").write_text(head + "\n", encoding="utf-8")
        self.assertEqual(self.pr("gh pr create --fill"), 0)
        git(self.repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "y")
        self.assertEqual(self.pr("gh pr create --fill"), 2)

    @unittest.skipIf(shutil.which("sh") is None, "sh not installed")
    def test_wrapper_forwards_the_block(self):
        payload = {"tool_name": "Bash", "tool_input": {"command": "gh pr create"}, "cwd": str(self.repo)}
        done = subprocess.run(["sh", str(HOOKS / "run.sh"), "pre_pr"], input=json.dumps(payload),
                              capture_output=True, text=True, timeout=30)
        self.assertEqual(done.returncode, 2)
        self.assertIn("/dev:audit diff", done.stderr)

    def test_other_commands_pass(self):
        self.assertEqual(self.pr("git status"), 0)
        self.assertEqual(self.pr("gh pr view 3"), 0)
        self.assertEqual(self.pr("gh pr create", tool="Read"), 0)


if __name__ == "__main__":
    unittest.main()
