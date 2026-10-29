"""Offline checks for the video scripts: corrupted-frame detection and music bed settings."""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "plugins/dev/skills"

try:
    import numpy as np
except ImportError:  # the CI image may not ship numpy
    np = None


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipIf(np is None, "numpy not installed")
class DeglitchTests(unittest.TestCase):
    def setUp(self):
        self.d = load("deglitch", "video-remotion/scripts/deglitch.py")

    def frames(self, n=60):
        # a slow horizontal drift: neighbouring frames differ a little
        base = np.tile(np.linspace(0, 255, 96, dtype=np.float32), (54, 1))
        return np.stack([np.roll(base, i, axis=1) for i in range(n)])

    def test_clean_motion_has_no_bad_run(self):
        self.assertEqual(self.d.bad_runs(self.frames()), [])

    def test_single_corrupted_frame_is_found(self):
        f = self.frames()
        f[20] = 255 - f[20]
        self.assertEqual(self.d.bad_runs(f), [(20, 1)])

    def test_three_frame_run_is_found_once(self):
        f = self.frames()
        f[30:33] = 0
        self.assertEqual(self.d.bad_runs(f), [(30, 3)])

    def test_scene_cut_is_not_a_glitch(self):
        f = self.frames()
        f[40:] = 255 - f[40:]
        self.assertEqual(self.d.bad_runs(f), [])


@unittest.skipIf(np is None, "numpy not installed")
class MusicBedTests(unittest.TestCase):
    def test_moods_are_five_note_chords_in_a_low_register(self):
        m = load("music_bed", "video-pedagogique/scripts/music_bed.py")
        self.assertEqual(set(m.MOODS), {"calme", "clair", "tension"})
        for chords in m.MOODS.values():
            for chord in chords:
                self.assertEqual(len(chord), 5)
                self.assertLess(max(m.hz(n) for n in chord), 800)
        self.assertAlmostEqual(m.hz(69), 440.0)


if __name__ == "__main__":
    unittest.main()
