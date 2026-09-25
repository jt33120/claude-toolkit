"""Ensure security scans target the project and report incomplete work."""

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/dev/skills/security/scripts/audit.py"
spec = importlib.util.spec_from_file_location("audit", SCRIPT)
audit = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = audit
spec.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_external_scans_use_project_requirements_and_separate_git_history(self):
        (self.root / "requirements.txt").write_text("requests==2.32.0\n")
        (self.root / ".git").mkdir()
        commands = []

        def run(command, **kwargs):
            commands.append(command)
            return subprocess.CompletedProcess(command, 0,
                                               '{"dependencies":[{"vulns":[]}]}\n' if command[0] == "pip-audit" else "", "")

        report = audit.Report()
        with patch.object(audit.shutil, "which", return_value="installed"), \
             patch.object(audit.subprocess, "run", side_effect=run):
            audit.run_external(report, self.root)
        self.assertIn(["pip-audit", "-f", "json", "-r", str(self.root / "requirements.txt")], commands)
        self.assertTrue(any(c[:2] == ["trufflehog", "filesystem"] for c in commands))
        self.assertTrue(any(c[:3] == ["trufflehog", "git", self.root.as_uri()] for c in commands))
        self.assertFalse(report.has_incomplete_scan)

    def test_failure_is_reported_instead_of_appearing_complete(self):
        (self.root / "requirements.txt").write_text("requests==2.32.0\n")
        with patch.object(audit.shutil, "which", return_value="installed"), \
             patch.object(audit.subprocess, "run", return_value=subprocess.CompletedProcess([], 4, "bad output", "error")):
            report = audit.Report()
            audit.run_external(report, self.root)
        self.assertTrue(report.has_incomplete_scan)
        self.assertIn("pip-audit-erreur", [finding.rule for finding in report.findings])
        self.assertIn("trufflehog-erreur", [finding.rule for finding in report.findings])

    def test_tracked_env_variant_is_critical(self):
        (self.root / ".git").mkdir()
        result = subprocess.CompletedProcess([], 0, "app/.env.production\0app/.env.example\0", "")
        with patch.object(audit.shutil, "which", return_value="git"), \
             patch.object(audit.subprocess, "run", return_value=result):
            report = audit.Report()
            audit.audit_env_git(self.root, report)
        self.assertEqual([f.location for f in report.findings if f.rule == "env-suivi-git"],
                         ["app/.env.production"])

    def test_git_check_failure_does_not_silently_pass(self):
        (self.root / ".git").mkdir()
        with patch.object(audit.shutil, "which", return_value="git"), \
             patch.object(audit.subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 20)):
            report = audit.Report()
            audit.audit_env_git(self.root, report)
        self.assertTrue(report.has_incomplete_scan)


if __name__ == "__main__":
    unittest.main()
