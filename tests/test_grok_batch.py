"""Offline checks for the Grok batch robot: shot list, resume, step config and stop conditions."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/dev/skills/video-remotion/scripts/grok_batch.py"
spec = importlib.util.spec_from_file_location("grok_batch", SCRIPT)
grok = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grok)

EXAMPLES = SCRIPT.parents[1] / "assets"
SHOT = {"id": "s01", "prompt": "a road", "type": "video", "ratio": "9:16"}


class GrokBatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.out = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, data):
        path = self.out / name
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_examples_are_valid(self):
        shots = grok.load_shots(EXAMPLES / "shots.example.json")
        config = json.loads((EXAMPLES / "grok_steps.example.json").read_text())
        for shot in shots:
            for step in config["steps"]:
                for value in [step.get("value"), *step.get("target", {}).values()]:
                    grok.render(value, shot)

    def test_rejects_duplicate_ids_and_missing_prompt(self):
        with self.assertRaises(SystemExit):
            grok.load_shots(self.write("a.json", [SHOT, SHOT]))
        with self.assertRaises(SystemExit):
            grok.load_shots(self.write("b.json", [{"id": "x"}]))

    def test_resume_skips_saved_media_only(self):
        (self.out / "s01.mp4").write_bytes(b"x")
        (self.out / "s02.json").write_text("{}")
        shots = [SHOT, {**SHOT, "id": "s02"}]
        self.assertEqual([s["id"] for s in grok.pending(shots, self.out)], ["s02"])

    def test_render_and_conditions(self):
        self.assertEqual(grok.render("{ratio}", SHOT), "9:16")
        with self.assertRaises(SystemExit):
            grok.render("{missing}", SHOT)
        self.assertTrue(grok.applies({"when": {"type": "video"}}, SHOT))
        self.assertFalse(grok.applies({"when": {"type": "image"}}, SHOT))

    def test_pause_parsing(self):
        self.assertEqual(grok.parse_pause("30-90"), (30.0, 90.0))
        self.assertEqual(grok.parse_pause("45"), (45.0, 45.0))
        with self.assertRaises(SystemExit):
            grok.parse_pause("90-30")

    def test_locate_maps_targets(self):
        page = MagicMock()
        grok.locate(page, {"role": "button", "name": "{ratio}"}, SHOT)
        page.get_by_role.assert_called_with("button", name="9:16", exact=False)
        grok.locate(page, {"css": "video", "nth": 0}, SHOT)
        page.locator.return_value.nth.assert_called_with(0)

    def test_visible_stop_condition_halts(self):
        page = MagicMock()
        page.get_by_text.return_value.first.is_visible.return_value = True
        with self.assertRaises(grok.Stop):
            grok.check_stops(page, {"stop_if_visible": [{"text": "limit"}]}, SHOT)

    def test_steps_without_save_stop(self):
        page = MagicMock()
        config = {"url": "u", "steps": [{"do": "wait", "seconds": 0}]}
        with self.assertRaises(grok.Stop):
            grok.run_shot(page, config, SHOT, self.out)

    def test_credit_logged_once(self):
        entry = {"file": "s01.mp4", "id": "s01", "prompt": "a road"}
        grok.record(self.out, entry)
        grok.record(self.out, entry)
        self.assertEqual(len(json.loads((self.out / "ai-credits.json").read_text())), 1)


if __name__ == "__main__":
    unittest.main()
