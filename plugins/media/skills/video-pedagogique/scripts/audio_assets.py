#!/usr/bin/env python3
"""Banque de bruitages et musique de fond générés avec ElevenLabs (sound-generation, music).

Usage : python3 audio_assets.py public/sfx public/audio/music.mp3 --music-secs 200 [--only whoosh impact]
Clé : ELEVENLABS_API_KEY (environnement ou ./.env). Un fichier déjà présent n'est jamais regénéré.
Durées des bruitages : 0,5 à 30 s (l'API refuse en dessous de 0,5 s).
Les bruitages se placent ensuite sur des mots de la timeline ; la musique se nivelle au mixage
(dynaudnorm) : voir references/son.md.
"""
import argparse, json, os, urllib.request
from pathlib import Path

SFX = {
    "whoosh": ("fast clean cinematic whoosh transition, airy swoosh", 1.0),
    "impact": ("deep cinematic boom impact hit with short tail, documentary trailer", 1.8),
    "typing": ("fast mechanical keyboard typing, close mic, office", 3.0),
    "ring": ("modern video call incoming ringtone, soft, two short rings", 2.5),
    "notif": ("soft modern UI notification ping", 0.8),
    "glitch": ("short digital glitch stutter, data corruption", 0.8),
    "alarm": ("subtle security alert beep, two tones, computer", 1.5),
    "coins": ("digital money transfer, quick cascade of coins and electronic swish", 1.6),
    "door": ("heavy wooden door slowly creaking open", 2.2),
    "stamp": ("rubber stamp hit hard on paper desk", 0.6),
    "pop": ("soft UI pop click", 0.5),
    "riser": ("short tension riser building up, cinematic", 2.0),
    "room": ("quiet modern open space office ambience, distant keyboards, air conditioning hum, no voices", 22.0),
}
MUSIC = ("Instrumental underscore for a modern cybersecurity explainer video. Steady 100 BPM pulse, tight soft electronic drums, "
         "warm mid-range synth plucks and a round bassline, light tension, subtle builds every 30 seconds, clear and present on laptop "
         "and phone speakers. No high-pitched leads, no bells, no vocals, no big drops. Leaves space for a male French voiceover.")


def key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k and Path(".env").exists():
        for line in Path(".env").read_text().splitlines():
            if line.startswith("ELEVENLABS_API_KEY="):
                k = line.split("=", 1)[1].strip()
    if not k:
        raise SystemExit("ELEVENLABS_API_KEY manquante")
    return k


def post(url, body, dest):
    if dest.exists() and dest.stat().st_size > 1000:
        print("déjà là :", dest); return
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"xi-api-key": key(), "Content-Type": "application/json"}, method="POST")
    try:
        dest.write_bytes(urllib.request.urlopen(req, timeout=900).read()); print("OK", dest)
    except Exception as ex:  # une erreur n'arrête pas le reste de la banque
        print("ERREUR", dest, ex, getattr(ex, "read", lambda: b"")()[:300])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sfx_dir"); ap.add_argument("music_out")
    ap.add_argument("--music-secs", type=float, default=200); ap.add_argument("--music-prompt", default=MUSIC)
    ap.add_argument("--only", nargs="*", help="noms de bruitages à générer (défaut : tous) ; « music » pour la musique seule")
    a = ap.parse_args()
    d = Path(a.sfx_dir); d.mkdir(parents=True, exist_ok=True)
    for name, (text, dur) in SFX.items():
        if a.only and name not in a.only:
            continue
        post("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128",
             {"text": text, "duration_seconds": dur, "prompt_influence": 0.5}, d / f"{name}.mp3")
    if not a.only or "music" in a.only:
        Path(a.music_out).parent.mkdir(parents=True, exist_ok=True)
        post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192",
             {"prompt": a.music_prompt, "music_length_ms": int(a.music_secs * 1000), "force_instrumental": True}, Path(a.music_out))
