#!/usr/bin/env python3
"""Find and repair corrupted frames in a rendered video (mosaic / duplicated-tile frames).

Headless Chrome sometimes rasterizes a frame wrongly (a tile of the image repeated, or a flash of
another screen), mostly with CSS `filter` or `mix-blend-mode` layers and under CPU load. Such a
frame is a short run (1 to 6 frames) that differs strongly from the frame before AND the frame
after, while the frames on both sides of the run look alike.

Usage:
    python3 deglitch.py check video.mp4 [more.mp4 ...]   # list suspect runs; exit 1 if any
    python3 deglitch.py fix in.mp4 out.mp4               # replace each bad frame by the last good one

`fix` re-encodes the picture losslessly enough for delivery (H.264 CRF 19) and copies the audio.
Run `check` again on the assembled final file: that is the number to report.
Needs numpy and ffmpeg/ffprobe.
"""
import argparse
import shutil
import subprocess
import sys

import numpy as np

W, H = 96, 54  # detection works on small grayscale frames


def small_frames(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)


def bad_runs(frames, jump=3.0, ratio=3.0, floor=2.5, longest=6):
    """Return (start, length) of runs that jump away and back while the surroundings agree."""
    mad = lambda a, b: float(np.abs(frames[a] - frames[b]).mean())
    runs, i = [], 1
    while i < len(frames) - 1:
        found = 0
        a = mad(i - 1, i)
        if a > jump:
            for length in range(1, longest + 1):
                if i + length >= len(frames):
                    break
                back = mad(i + length - 1, i + length)
                around = mad(i - 1, i + length)
                if min(a, back) > ratio * around + floor:
                    runs.append((i, length))
                    found = length
                    break
        i += found or 1
    return runs


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate", "-of", "default=nw=1", path]).decode()
    info = dict(line.split("=", 1) for line in out.split() if "=" in line)
    return int(info["width"]), int(info["height"]), info["r_frame_rate"]


def check(paths):
    total = 0
    for path in paths:
        frames = small_frames(path)
        runs = bad_runs(frames)
        total += len(runs)
        _, _, rate = probe(path)
        num, den = (int(x) for x in rate.split("/"))
        where = " ".join(f"{start * den / num:.2f}s(x{length})" for start, length in runs[:40])
        print(f"{path}: frames={len(frames)} bad_runs={len(runs)} {where}".rstrip())
    print(f"TOTAL {total}")
    return 1 if total else 0


def fix(src, dst):
    runs = bad_runs(small_frames(src))
    if not runs:
        shutil.copyfile(src, dst)
        print("0 frame replaced")
        return 0
    bad = {start + k for start, length in runs for k in range(length)}
    w, h, rate = probe(src)
    size = w * h * 3
    reader = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                              stdout=subprocess.PIPE)
    writer = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                               "-r", rate, "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264",
                               "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy",
                               "-movflags", "+faststart", dst], stdin=subprocess.PIPE)
    last, index = None, 0
    while True:
        buf = reader.stdout.read(size)
        if len(buf) < size:
            break
        if index in bad and last is not None:
            buf = last
        else:
            last = buf
        writer.stdin.write(buf)
        index += 1
    reader.wait()
    writer.stdin.close()
    writer.wait()
    left = bad_runs(small_frames(dst))
    print(f"{len(bad)} frame(s) replaced in {len(runs)} run(s); remaining: {len(left)}")
    return 1 if left else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("paths", nargs="+")
    f = sub.add_parser("fix")
    f.add_argument("src")
    f.add_argument("dst")
    args = parser.parse_args()
    sys.exit(check(args.paths) if args.cmd == "check" else fix(args.src, args.dst))
