#!/usr/bin/env python3
"""Planche de contrôle : extrait une image toutes les N secondes d'une vidéo et les assemble.

Usage : python3 contact_sheet.py video.mp4 out/sheet.png [--every 1.6] [--cols 7] [--width 270]
Demande ffmpeg/ffprobe et Pillow. Chaque vignette porte son instant en jaune. Regarder la planche
pour de vrai : écrans vides, chevauchements avec les sous-titres, textes coupés, flashs rectangulaires.
"""
import subprocess, sys, tempfile
from pathlib import Path
from PIL import Image, ImageDraw

opts = {"--every": 1.6, "--cols": 7, "--width": 270}
argv = sys.argv[1:]
pos = []
i = 0
while i < len(argv):
    if argv[i] in opts:
        opts[argv[i]] = type(opts[argv[i]])(argv[i + 1]); i += 2
    else:
        pos.append(argv[i]); i += 1
if len(pos) < 2:
    sys.exit(__doc__)
video, out = pos[0], pos[1]
every, cols, width = opts["--every"], opts["--cols"], opts["--width"]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video]))
height = int(width * 1350 / 1080)
tmp = Path(tempfile.mkdtemp())
ims, t = [], 0.3
while t < dur:
    p = tmp / f"{t:.1f}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1", "-vf", f"scale={width}:{height}", str(p)], check=True)
    im = Image.open(p).convert("RGB"); ImageDraw.Draw(im).text((4, height - 16), f"{t:.1f}s", fill="yellow"); ims.append(im)
    t += every
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (width * cols, height * rows), "white")
for k, im in enumerate(ims):
    sheet.paste(im, ((k % cols) * width, (k // cols) * height))
Path(out).parent.mkdir(parents=True, exist_ok=True)
sheet.save(out)
print(f"OK → {out} ({len(ims)} images, {rows} lignes)")
