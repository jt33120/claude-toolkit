#!/usr/bin/env python3
"""Bruitages synthétisés (aucun échantillon externe, aucune IA) calés sur des mots de la voix.

À lancer depuis la racine du projet Remotion. Lit edition/edition.json (« sfx » : liste de
{scene, word, type, nth?, pre?, delay?, n?, gap?} ; « musicMute » : id de la scène où la musique se tait)
et edition/words.json. Écrit public/audio/sfx.wav (durée de la vidéo) et out/mixmeta.json
({"music_mute": [début, fin]} en secondes vidéo), que le mixage lit pour couper la musique.
Types : impact, stamp, whoosh, riser, tick, ticks (rafale), click, pop.

Usage : python3 sfx.py out/timeline.json      (timeline.json : {"fps", "total", "lead"} en frames)
"""
import json, math, re, sys, unicodedata, wave
from pathlib import Path
import struct, random

if len(sys.argv) < 2:
    sys.exit(__doc__)
ROOT = Path.cwd()
SR = 48000
tl = json.loads(Path(sys.argv[1]).read_text())
lead = tl["lead"] / tl["fps"]
total = tl["total"] / tl["fps"]
ed = json.loads((ROOT / "edition/edition.json").read_text(encoding="utf-8"))
words = json.loads((ROOT / "edition/words.json").read_text(encoding="utf-8"))["words"]

def norm(x):
    x = re.sub(r"^(l|d|qu|c|s|n|j|m|t)['’]", "", x.lower())
    x = "".join(ch for ch in unicodedata.normalize("NFD", x) if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]", "", x)

def find(scene, pref, nth=0):
    hits = [w for w in words if w["scene"] == scene and norm(w["word"]).startswith(norm(pref))]
    return hits[nth]["start"] + lead if len(hits) > nth else None

buf = [0.0] * int((total + 1) * SR)
rng = random.Random(7)

def add(t0, samples, gain):
    i0 = int(t0 * SR)
    for k, v in enumerate(samples):
        if 0 <= i0 + k < len(buf):
            buf[i0 + k] += v * gain

def env(n, a, d):
    out = []
    for k in range(n):
        t = k / SR
        out.append(min(1.0, t / a) if t < a else math.exp(-(t - a) / d))
    return out

def impact():
    n = int(0.55 * SR); e = env(n, 0.004, 0.12); ph = 0.0; s = []
    for k in range(n):
        f = 70 - 35 * (k / n); ph += 2 * math.pi * f / SR
        click = rng.uniform(-1, 1) * math.exp(-k / (0.012 * SR))
        s.append(e[k] * (0.9 * math.sin(ph)) + 0.35 * click)
    return s

def whoosh(dur=0.38):
    n = int(dur * SR); s = []; lp = 0.0
    for k in range(n):
        x = k / n; a = math.sin(math.pi * x) ** 2
        alpha = 0.02 + 0.25 * x  # filtre qui s'ouvre : effet de passage
        lp += alpha * (rng.uniform(-1, 1) - lp)
        s.append(a * lp * 2.2)
    return s

def riser(dur=0.9):
    n = int(dur * SR); s = []; ph = 0.0; lp = 0.0
    for k in range(n):
        x = k / n; f = 180 + 900 * x * x; ph += 2 * math.pi * f / SR
        lp += 0.08 * (rng.uniform(-1, 1) - lp)
        s.append((x ** 1.5) * (0.35 * math.sin(ph) + 0.8 * lp) * (1 - max(0, x - 0.95) * 20))
    return s

def tone(f0, f1, dur, d):
    n = int(dur * SR); e = env(n, 0.002, d); ph = 0.0; s = []
    for k in range(n):
        f = f0 + (f1 - f0) * k / n; ph += 2 * math.pi * f / SR; s.append(e[k] * math.sin(ph))
    return s

KIND = {
    "impact": (impact, 0.55), "stamp": (impact, 0.45), "whoosh": (whoosh, 0.35), "riser": (riser, 0.22),
    "tick": (lambda: tone(2200, 2000, 0.05, 0.012), 0.18), "click": (lambda: tone(3200, 2600, 0.03, 0.006), 0.25),
    "pop": (lambda: tone(700, 180, 0.12, 0.04), 0.4),
}
placed = 0
for c in ed.get("sfx", []):
    t = find(c["scene"], c["word"], c.get("nth", 0))
    if t is None:
        print("mot introuvable :", c); continue
    t = t - c.get("pre", 0) + c.get("delay", 0)
    if c["type"] == "ticks":
        for j in range(c.get("n", 8)):
            add(t + j * c.get("gap", 0.08), tone(2400, 2100, 0.04, 0.01), 0.12); placed += 1
        continue
    fn, g = KIND[c["type"]]
    add(t, fn(), g); placed += 1

peak = max(1e-9, max(abs(v) for v in buf))
scale = min(1.0, 0.89 / peak)
out = ROOT / "public/audio/sfx.wav"
out.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(out), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, v * scale)) * 32767)) for v in buf))
meta = {}
ms = ed.get("musicMute")
if ms:
    sw = [w for w in words if w["scene"] == ms]
    if sw:
        meta["music_mute"] = [round(sw[0]["start"] + lead - 0.25, 3), round(sw[-1]["end"] + lead + 0.35, 3)]
(ROOT / "out").mkdir(exist_ok=True)
(ROOT / "out/mixmeta.json").write_text(json.dumps(meta))
print(f"OK → public/audio/sfx.wav ({placed} sons), mixmeta {meta}")
