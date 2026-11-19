#!/usr/bin/env python3
"""Join scene files into one video by re-encoding, then optionally make a size-capped copy.

Scenes rendered separately carry their own timestamps; joining them with `-c copy` (concat demuxer)
can give a file whose reported duration is several times too long. This script decodes every scene
and re-encodes through ffmpeg's concat filter, so the result is always the sum of the scenes.

Usage:
    python3 assemble.py out/final.mp4 out/scenes/s00.mp4 out/scenes/s01.mp4 ...
        [--crf 19] [--cap-mb 18.5 --cap-out out/web.mp4 --cap-width 960]

`--cap-mb` writes a second file under that size (MB = 10^6 bytes, audio AAC 48 kbit/s mono),
with the video bitrate computed from the duration. Prints duration, loudness and peak.
Needs ffmpeg/ffprobe.
"""
import argparse
import os
import re
import subprocess


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", path]).decode().strip().strip(","))


def join(out, scenes, crf, fps):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    for scene in scenes:
        cmd += ["-i", scene]
    graph = "".join(f"[{i}:v:0]fps={fps},format=yuv420p,setsar=1[v{i}];"
                    f"[{i}:a:0]aresample=48000,aformat=channel_layouts=stereo[a{i}];" for i in range(len(scenes)))
    graph += "".join(f"[v{i}][a{i}]" for i in range(len(scenes))) + f"concat=n={len(scenes)}:v=1:a=1[v][a]"
    cmd += ["-filter_complex", graph, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", str(crf),
            "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)


def loudness(path):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    summary = log[log.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", summary)
    p = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary)
    return (float(i.group(1)) if i else None), (float(p.group(1)) if p else None)


def capped(src, out, megabytes, width):
    dur = duration(src)
    kbps = max(150, int(megabytes * 8 * 1000 / dur - 48))  # total budget minus 48 kbit/s audio
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", f"scale={width}:-2", "-c:v", "libx264",
                    "-preset", "slow", "-b:v", f"{kbps}k", "-maxrate", f"{kbps * 2}k", "-bufsize", f"{kbps * 4}k",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "48k", "-ac", "1", "-movflags", "+faststart", out],
                   check=True)
    return kbps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out")
    parser.add_argument("scenes", nargs="+")
    parser.add_argument("--crf", type=int, default=19)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--cap-mb", type=float)
    parser.add_argument("--cap-out")
    parser.add_argument("--cap-width", type=int, default=960)
    args = parser.parse_args()
    join(args.out, args.scenes, args.crf, args.fps)
    expected = sum(duration(s) for s in args.scenes)
    got = duration(args.out)
    lufs, peak = loudness(args.out)
    print(f"{args.out}: {got:.2f} s (scenes {expected:.2f} s), {lufs} LUFS, peak {peak} dBFS")
    if args.cap_mb and args.cap_out:
        kbps = capped(args.out, args.cap_out, args.cap_mb, args.cap_width)
        print(f"{args.cap_out}: {kbps} kbit/s video, {os.path.getsize(args.cap_out) / 1e6:.1f} MB")
