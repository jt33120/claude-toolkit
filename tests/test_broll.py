"""Offline checks for B-roll clip selection, credits and key handling."""

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/dev/skills/video-remotion/scripts/broll.py"
spec = importlib.util.spec_from_file_location("broll", SCRIPT)
broll = importlib.util.module_from_spec(spec)
spec.loader.exec_module(broll)

PEXELS_ITEM = {
    "id": 1, "url": "https://www.pexels.com/video/x-1/", "duration": 12,
    "user": {"name": "Ana", "url": "https://www.pexels.com/@ana"},
    "video_files": [
        {"link": "sd", "width": 640, "height": 360, "file_type": "video/mp4"},
        {"link": "hd", "width": 1920, "height": 1080, "file_type": "video/mp4"},
        {"link": "uhd", "width": 3840, "height": 2160, "file_type": "video/mp4"},
        {"link": "hls", "width": 1920, "height": 1080, "file_type": "application/x-mpegURL"},
    ],
}


class BrollTests(unittest.TestCase):
    def test_pexels_picks_smallest_file_that_reaches_target(self):
        self.assertEqual(broll.pexels_clip(PEXELS_ITEM)["download_url"], "hd")
        self.assertEqual(broll.pexels_clip(PEXELS_ITEM, 3000)["download_url"], "uhd")

    def test_falls_back_to_largest_when_target_unreachable(self):
        self.assertEqual(broll.pexels_clip(PEXELS_ITEM, 9999)["download_url"], "uhd")

    def test_pixabay_skips_empty_tiers(self):
        item = {"id": 2, "pageURL": "p", "user": "Bo", "duration": 8, "videos": {
            "large": {"url": "", "width": 0, "height": 0},
            "medium": {"url": "m", "width": 1920, "height": 1080},
            "small": {"url": "s", "width": 1280, "height": 720}}}
        self.assertEqual(broll.pixabay_clip(item)["download_url"], "m")

    def test_missing_key_exits_without_leaking(self):
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(SystemExit) as ctx:
            broll.api_key("pexels")
        self.assertIn("PEXELS_API_KEY", str(ctx.exception))

    def test_credit_is_recorded_once_per_file(self):
        clip = broll.pexels_clip(PEXELS_ITEM)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            broll.record_credit(out, clip, "pexels-1.mp4")
            broll.record_credit(out, clip, "pexels-1.mp4")
            credits = json.loads((out / "credits.json").read_text())
        self.assertEqual(len(credits), 1)
        self.assertEqual(credits[0]["author"], "Ana")
        self.assertIn("Pexels License", credits[0]["license"])


if __name__ == "__main__":
    unittest.main()
