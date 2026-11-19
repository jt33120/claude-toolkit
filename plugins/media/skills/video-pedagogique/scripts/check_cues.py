#!/usr/bin/env python3
"""Vérifie les mots déclencheurs d'une vidéo Remotion calée sur la voix, et mesure les trous.

Usage : python3 check_cues.py src/scenes/ma-video.tsx edition/edition.json edition/words.json [--max-gap 2.5]

- Chaque composant de scène `const X: React.FC<P> = ({ scene }) => { … }` est relié à la scène
  d'edition.json dont le champ `type` vaut X ; chaque `cue(scene, "mot"[, n])` doit trouver le n-ième
  mot de cette scène qui commence par « mot » (même normalisation que timeline.ts : minuscules, sans
  accents ni ponctuation, élision l'/d'/qu' retirée).
- Affiche l'instant de chaque déclencheur et, par scène, le plus long trou entre deux déclencheurs
  (début et fin de scène compris). Code de sortie 1 si un mot manque ou si un trou dépasse --max-gap.
"""
import json, re, sys, unicodedata

args = [a for a in sys.argv[1:] if not a.startswith("--")]
max_gap = float(sys.argv[sys.argv.index("--max-gap") + 1]) if "--max-gap" in sys.argv else 2.5
if "--max-gap" in sys.argv:
    args = [a for a in args if a != sys.argv[sys.argv.index("--max-gap") + 1]]
if len(args) < 3:
    sys.exit(__doc__)
src = open(args[0], encoding="utf-8").read()
ed = json.load(open(args[1], encoding="utf-8"))
words = json.load(open(args[2], encoding="utf-8"))["words"]

def norm(x):
    x = re.sub(r"^(l|d|qu|c|s|n|j|m|t)['’]", "", x.lower())
    x = "".join(ch for ch in unicodedata.normalize("NFD", x) if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]", "", x)

types = {s["type"]: s["id"] for s in ed["scenes"]}
ok = True
for m in re.finditer(r"const (\w+): React\.FC<P> = \(\{ scene \}\) => \{(.*?)\n\};", src, re.S):
    typ, body = m.group(1), m.group(2)
    sid = types.get(typ)
    if not sid:
        continue
    ws = [w for w in words if w["scene"] == sid]
    if not ws:
        continue
    times = []
    for c in re.finditer(r'cue\(scene, "([^"]+)"(?:, (\d+))?\)', body):
        pref, nth = norm(c.group(1)), int(c.group(2) or 0)
        hits = [w for w in ws if norm(w["word"]).startswith(pref)]
        if len(hits) <= nth:
            print(f"MANQUANT  {typ}: « {c.group(1)} »"); ok = False; continue
        t = hits[nth]["start"]; times.append(t)
        print(f"{typ:14s} {c.group(1):16s} {t:6.2f} s  ({hits[nth]['word']})")
    marks = sorted(set([ws[0]["start"], ws[-1]["end"]] + times))
    gaps = [(b - a, a) for a, b in zip(marks, marks[1:])]
    if gaps:
        g, at = max(gaps)
        flag = "  TROU À COMBLER" if g > max_gap else ""
        if flag:
            ok = False
        print(f"{'':14s} plus long trou {g:4.1f} s à partir de {at:5.2f} s{flag}")
print("OK" if ok else "ERREURS")
sys.exit(0 if ok else 1)
