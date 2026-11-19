#!/usr/bin/env python3
"""Voix off en une seule prise ElevenLabs (eleven_multilingual_v2), pauses écrites avec <break>.

Trois commandes :
  gen    edition.json -> une prise par graine (take<seed>.json + take<seed>.mp3), texte complet avec pauses
  check  compare la transcription (speech-to-text) de chaque prise au script : mots répétés, sautés, déformés
  words  prise choisie -> words.json mot par mot et par scène (format attendu par check_cues.py et la timeline)

edition.json : { "scenes": [ { "id": "...", "narration": "...", "pause": 0.6 } ] }
  « pause » = silence après la scène (secondes). Des pauses internes peuvent être écrites directement
  dans la narration avec <break time="0.5s" /> ; elles sont retirées avant le découpage en mots.

Clé : variable d'environnement ELEVENLABS_API_KEY, ou ligne ELEVENLABS_API_KEY= dans ./.env.
Coût : ≈ 1 crédit par caractère et par prise ; « check » consomme du temps de transcription.

Exemples :
  python3 voice_take.py gen edition/edition.json out/voice --voice <voice_id> --seeds 11 23
  python3 voice_take.py check edition/edition.json out/voice --seeds 11 23
  python3 voice_take.py words edition/edition.json out/voice --seed 11 --out edition/words.json
"""
import argparse, base64, difflib, json, os, re, subprocess, unicodedata, urllib.request, uuid
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
TAG = re.compile(r'<break[^>]*/>')


def key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k and Path(".env").exists():
        for line in Path(".env").read_text().splitlines():
            if line.startswith("ELEVENLABS_API_KEY="):
                k = line.split("=", 1)[1].strip()
    if not k:
        raise SystemExit("ELEVENLABS_API_KEY manquante")
    return k


def full_text(ed):
    parts = []
    for s in ed["scenes"]:
        t = (s.get("narration") or "").strip()
        if not t:
            continue
        p = s.get("pause")
        parts.append(t + (f' <break time="{p}s" />' if p else ""))
    return " ".join(parts)


def post(url, body, headers):
    req = urllib.request.Request(url, data=body, headers={"xi-api-key": key(), **headers}, method="POST")
    return urllib.request.urlopen(req, timeout=900).read()


def gen(a):
    ed = json.loads(Path(a.edition).read_text())
    text = full_text(ed)
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    (out / "full_text.txt").write_text(text)
    print(f"{len(text)} caractères × {len(a.seeds)} prises ≈ {len(text) * len(a.seeds)} crédits")
    for seed in a.seeds:
        dest = out / f"take{seed}.json"
        if dest.exists():
            print("déjà là :", dest); continue
        body = {"text": text, "model_id": a.model, "language_code": a.lang, "seed": seed,
                "voice_settings": {"stability": a.stability, "similarity_boost": a.similarity, "style": a.style,
                                   "use_speaker_boost": True, "speed": a.speed}}
        raw = post(f"{API}/text-to-speech/{a.voice}/with-timestamps?output_format=mp3_44100_128",
                   json.dumps(body).encode(), {"Content-Type": "application/json"})
        dest.write_bytes(raw)
        (out / f"take{seed}.mp3").write_bytes(base64.b64decode(json.loads(raw)["audio_base64"]))
        print("OK prise", seed)


def toks(s):
    s = unicodedata.normalize("NFD", TAG.sub(" ", s).lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", s)


def check(a):
    ed = json.loads(Path(a.edition).read_text())
    ref = toks(full_text(ed))
    out = Path(a.outdir)
    for seed in a.seeds:
        mp3 = out / f"take{seed}.mp3"
        stt = out / f"stt{seed}.json"
        if not stt.exists():
            b = uuid.uuid4().hex
            data = b"".join([
                f'--{b}\r\nContent-Disposition: form-data; name="model_id"\r\n\r\nscribe_v1\r\n'.encode(),
                f'--{b}\r\nContent-Disposition: form-data; name="language_code"\r\n\r\n{a.lang}\r\n'.encode(),
                f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{mp3.name}"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()
                + mp3.read_bytes() + b"\r\n", f"--{b}--\r\n".encode()])
            stt.write_bytes(post(f"{API}/speech-to-text", data, {"Content-Type": f"multipart/form-data; boundary={b}"}))
        hyp = toks(json.loads(stt.read_text())["text"])
        sm = difflib.SequenceMatcher(a=ref, b=hyp, autojunk=False)
        diffs = [(op, " ".join(ref[i1:i2]), " ".join(hyp[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
        print(f"prise {seed} : similarité {sm.ratio():.3f}, {len(diffs)} écarts (chiffres en toutes lettres et pluriels = normal)")
        for d in diffs:
            print("   ", d)
        al = json.loads((out / f"take{seed}.json").read_text())["alignment"]
        st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
        long_gaps = [round(st[i] - en[i - 1], 2) for i in range(1, len(st)) if st[i] - en[i - 1] > 1.2]
        print("    silences > 1,2 s hors pauses écrites :", long_gaps or "aucun")


def words(a):
    ed = json.loads(Path(a.edition).read_text())
    text = full_text(ed)
    take = json.loads((Path(a.outdir) / f"take{a.seed}.json").read_text())
    al = take["alignment"]
    if "".join(al["characters"]) != text:
        raise SystemExit("l'alignement ne correspond pas au texte : edition.json a changé depuis la génération")
    st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    out, cur = [], 0
    for s in ed["scenes"]:
        for w in TAG.sub(" ", s.get("narration") or "").split():
            i = text.find(w, cur)
            if i < 0:
                raise SystemExit(f"mot introuvable : {s['id']} / {w}")
            j = i + len(w) - 1
            out.append({"word": w, "start": round(st[i], 3), "end": round(en[j], 3), "scene": s["id"]})
            cur = j + 1
    mp3 = Path(a.outdir) / f"take{a.seed}.mp3"
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
                               capture_output=True, text=True).stdout or 0)
    Path(a.out).write_text(json.dumps({"model": "eleven_multilingual_v2", "source": f"take{a.seed}", "duration": round(dur, 3),
                                       "words": out}, ensure_ascii=False, indent=1))
    print(f"{len(out)} mots, {dur:.1f} s -> {a.out} ; voix : {mp3}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen"); g.add_argument("edition"); g.add_argument("outdir"); g.add_argument("--voice", required=True)
    g.add_argument("--seeds", type=int, nargs="+", default=[11, 23]); g.add_argument("--model", default="eleven_multilingual_v2")
    g.add_argument("--lang", default="fr"); g.add_argument("--stability", type=float, default=0.4)
    g.add_argument("--similarity", type=float, default=0.8); g.add_argument("--style", type=float, default=0.4)
    g.add_argument("--speed", type=float, default=1.0)
    c = sub.add_parser("check"); c.add_argument("edition"); c.add_argument("outdir"); c.add_argument("--seeds", type=int, nargs="+", default=[11, 23])
    c.add_argument("--lang", default="fr")
    w = sub.add_parser("words"); w.add_argument("edition"); w.add_argument("outdir"); w.add_argument("--seed", type=int, required=True)
    w.add_argument("--out", default="edition/words.json")
    a = ap.parse_args()
    {"gen": gen, "check": check, "words": words}[a.cmd](a)
