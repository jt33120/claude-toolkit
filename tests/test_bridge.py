"""Behavior checks for non-destructive bridge migration and refreshes."""

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/core/skills/agent-bridge/scripts/bridge.py"
spec = importlib.util.spec_from_file_location("bridge", SCRIPT)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.before = Path.cwd()
        os.chdir(self.root)
        bridge.APPLY = True

    def tearDown(self):
        os.chdir(self.before)
        bridge.APPLY = False
        self.temp.cleanup()

    def test_existing_claude_file_is_preserved_for_manual_migration(self):
        old = "# Specific Claude instructions\nKeep this setting.\n"
        Path("CLAUDE.md").write_text(old)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            bridge.context()
        self.assertIn("manually move", output.getvalue())
        self.assertEqual(Path("CLAUDE.md").read_text(), old)
        self.assertFalse(Path("AGENTS.md").exists())

    def test_import_added_once_without_discarding_original(self):
        Path("AGENTS.md").write_text("# Shared rules\n")
        Path("CLAUDE.md").write_text("# Claude only\nLeave unchanged\n")
        bridge.context()
        bridge.context()
        self.assertEqual(Path("CLAUDE.md").read_text(),
                         "@AGENTS.md\n\n# Claude only\nLeave unchanged\n")

    def test_dry_run_does_not_create_or_change_files(self):
        Path("AGENTS.md").write_text("shared\n")
        Path("CLAUDE.md").write_text("claude\n")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            bridge.main(["context"])
        self.assertIn("DRY", output.getvalue())
        self.assertEqual(Path("CLAUDE.md").read_text(), "claude\n")

    def test_symlinked_claude_file_requires_manual_review(self):
        linked = self.root / "outside.md"
        linked.write_text("outside\n")
        Path("AGENTS.md").write_text("shared\n")
        Path("CLAUDE.md").symlink_to(linked)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            bridge.context()
        self.assertIn("symlink", output.getvalue())
        self.assertEqual(linked.read_text(), "outside\n")

    def test_windows_copy_refreshes_only_when_unmodified(self):
        source = self.root / "source"
        source.mkdir()
        (source / "SKILL.md").write_text("v1")
        target = self.root / "target"
        with patch.object(bridge.Path, "symlink_to", side_effect=OSError("no permission")):
            bridge.link(source, target)
        self.assertEqual((target / "SKILL.md").read_text(), "v1")
        self.assertTrue((target / bridge.MARKER).is_file())
        (source / "SKILL.md").write_text("v2")
        bridge.link(source, target)
        self.assertEqual((target / "SKILL.md").read_text(), "v2")
        (target / "SKILL.md").write_text("my edits")
        (source / "SKILL.md").write_text("v3")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            bridge.link(source, target)
        self.assertIn("local changes", output.getvalue())
        self.assertEqual((target / "SKILL.md").read_text(), "my edits")

    def test_mcp_forwards_only_environment_names(self):
        config = {"mcpServers": {
            "good": {"command": "example", "args": ["--stdio"],
                     "env": {"SERVICE_TOKEN": "very-private-value"}},
            "unsafe": {"url": "https://example.com/mcp?token=very-private-value"},
            "arg": {"command": "example", "args": ["--token=very-private-value"]},
        }}
        Path(".mcp.json").write_text(json.dumps(config))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            bridge.mcp()
        result = output.getvalue()
        self.assertIn('env_vars = ["SERVICE_TOKEN"]', result)
        self.assertNotIn("very-private-value", result)
        self.assertNotIn("[mcp_servers.unsafe]", result)
        self.assertNotIn("[mcp_servers.arg]", result)


if __name__ == "__main__":
    unittest.main()
