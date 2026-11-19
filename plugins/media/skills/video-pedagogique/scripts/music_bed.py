#!/usr/bin/env python3
"""Musique de fond synthétisée (aucun échantillon, aucune licence) et mixage sous la voix.

Une nappe d'accords lente, sans mélodie qui accroche, qui respire un peu ; quelques notes
claires et rares par-dessus. Faite pour rester sous une voix sans lui disputer l'attention.

  make : python3 music_bed.py make --dur 397.5 --mood calme --lufs -32 bed.wav
  mix  : python3 music_bed.py mix video.mp4 bed.wav out.mp4 [--mute 28.0-34.5] [--abr 192k] [--ac 2]

Ambiances : calme (cours, explication longue), clair (news, démo produit), tension (accroche, incident).
Niveau : --lufs = loudness du programme moins 16 dB (cours à −16 LUFS → −32 ; réseaux à −14 → −30) ;
après le compresseur latéral, la musique est ≈ 21 dB sous la voix quand elle parle (mesuré sur un cours réel),
≈ 16 dB sous la voix dans les pauses. Plus discret : moins 18 à 20 dB. Le mixage
copie l'image sans la ré-encoder et limite les crêtes à −1,5 dBFS. --mute coupe la musique
sur un intervalle (en secondes), par exemple la phrase clé d'une news.
Dépendances : numpy, ffmpeg.
"""
import argparse, os, subprocess, sys, tempfile, wave
import numpy as np

SR = 24000  # la nappe n'a rien au-dessus de 5 kHz ; ffmpeg rééchantillonne en 48 kHz à la sortie

MOODS = {  # accords (notes MIDI), un toutes les `chord` secondes, en boucle
    "calme": [[41, 53, 57, 60, 64], [45, 52, 55, 60, 64], [36, 52, 55, 59, 64], [47, 50, 55, 59, 64]],
    "clair": [[48, 55, 59, 62, 64], [45, 52, 57, 60, 64], [41, 53, 57, 60, 65], [43, 50, 55, 59, 62]],
    "tension": [[38, 45, 50, 53, 57], [34, 46, 50, 53, 57], [43, 50, 55, 58, 62], [45, 52, 57, 61, 64]],
}


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tone(f, t):
    # sinus doux + deux harmoniques faibles : rond, sans attaque
    w = 2 * np.pi * f * t
    return np.sin(w) + 0.15 * np.sin(2 * w) + 0.05 * np.sin(3 * w)


def make(dur, mood, lufs, out, chord=8.0, seed=7):
    rng = np.random.default_rng(seed)
    n = int((dur + 1) * SR)
    L = np.zeros(n); R = np.zeros(n)
    xf = 2.5  # fondu enchaîné entre accords
    prog = MOODS[mood]
    k = 0
    t0 = 0.0
    while t0 < dur + 1:
        a, b = max(0.0, t0 - xf), min(dur + 1, t0 + chord + xf)
        i0, i1 = int(a * SR), int(b * SR)
        t = np.arange(i0, i1) / SR
        # montée sur [t0 - xf, t0 + xf], descente sur [t0 + chord - xf, t0 + chord + xf] : deux accords voisins somment à 1
        up = np.clip((t - (t0 - xf)) / (2 * xf), 0, 1)
        dn = np.clip((t0 + chord + xf - t) / (2 * xf), 0, 1)
        env = (0.5 - 0.5 * np.cos(np.pi * up)) * (0.5 - 0.5 * np.cos(np.pi * dn))
        if t0 == 0:
            env = np.where(t < chord, 1.0, env)
        for j, m in enumerate(prog[k % len(prog)]):
            g = 0.32 if j == 0 else 0.2
            for cents, pan in ((-6, 0.8), (0, 0.5), (6, 0.2)):
                s = g * tone(hz(m) * 2 ** (cents / 1200), t) * env
                L[i0:i1] += s * pan
                R[i0:i1] += s * (1 - pan)
        t0 += chord
        k += 1
    # notes claires, rares et aléatoires (graine fixe : même musique à chaque fois)
    t = rng.uniform(1.5, 4.0)
    while t < dur - 2:
        if rng.random() < 0.55:
            chord_now = prog[int(t // chord) % len(prog)]
            m = int(rng.choice(chord_now[2:])) + 12
            i0 = int(t * SR)
            d = np.arange(int(2.5 * SR)) / SR
            s = 0.09 * np.sin(2 * np.pi * hz(m) * d) * np.exp(-d / 0.9) * np.minimum(1, d / 0.02)
            i1 = min(n, i0 + len(s))
            pan = rng.uniform(0.3, 0.7)
            L[i0:i1] += s[: i1 - i0] * pan
            R[i0:i1] += s[: i1 - i0] * (1 - pan)
        t += rng.uniform(1.5, 4.0)
    tt = np.arange(n) / SR
    breath = 1 + 0.12 * np.sin(2 * np.pi * tt / 23.0)
    st = np.stack([L * breath, R * breath], axis=1)
    st /= np.max(np.abs(st)) + 1e-9
    pcm = (st * 0.7 * 32767).astype("<i2")
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "raw.wav")
        with wave.open(raw, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
        af = (f"highpass=f=70,lowpass=f=3500,aecho=0.8:0.6:90|170:0.25|0.15,"
              f"atrim=0:{dur},afade=t=in:d=3,afade=t=out:st={max(0, dur - 4)}:d=4,"
              f"loudnorm=I={lufs}:TP=-9:LRA=7,aresample=48000")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ar", "48000", out], check=True)
    print(f"{out} : {dur:.1f} s, ambiance {mood}, {lufs} LUFS")


def mix(video, bed, out, mute=None, abr="192k", ac=2):
    af = "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo"  # sans ça, sidechaincompress refuse des formats différents
    m = f"[1:a]{af}[m0]"
    if mute:
        a, b = (float(x) for x in mute.split("-"))
        m = f"[1:a]{af},volume='if(between(t,{a},{b}),0,1)':eval=frame[m0]"
    fc = (f"{m};[0:a]{af},asplit=2[v][k];[m0][k]sidechaincompress=threshold=0.05:ratio=2:attack=40:release=700[md];"
          f"[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.84:level=false[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", bed, "-filter_complex", fc,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", abr, "-ar", "48000",
                    "-ac", str(ac), "-movflags", "+faststart", out], check=True)
    print(f"{out} : musique mixée sous la voix")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    pm = sub.add_parser("make")
    pm.add_argument("out")
    pm.add_argument("--dur", type=float, required=True)
    pm.add_argument("--mood", choices=sorted(MOODS), default="calme")
    pm.add_argument("--lufs", type=float, default=-32)
    pm.add_argument("--seed", type=int, default=7)
    px = sub.add_parser("mix")
    px.add_argument("video"); px.add_argument("bed"); px.add_argument("out")
    px.add_argument("--mute")
    px.add_argument("--abr", default="192k")
    px.add_argument("--ac", type=int, default=2)
    a = p.parse_args()
    if a.cmd == "make":
        make(a.dur, a.mood, a.lufs, a.out, seed=a.seed)
    else:
        mix(a.video, a.bed, a.out, a.mute, a.abr, a.ac)
