#!/usr/bin/env python3
"""Deterministic AI-writing tells checker (FR + EN). Stdlib only.

Usage: python3 ai_tells.py FILE|- [--lang fr|en|auto] [--voice .claude/voice.md] [--min-score 80]
Prints a 0-100 score (100 = no tell found) and findings with line numbers.
Exit code 1 if the score is below --min-score.
"""
import argparse, re, statistics, sys

PHRASES = {
    "fr": [
        r"il ne s'agit pas (seulement|simplement|uniquement) de", r"non seulement\b.*\bmais (aussi|également)",
        r"n'hésitez pas à", r"plongeons", r"dans (le paysage|l'univers|le monde) (actuel|en constante évolution)",
        r"en (somme|conclusion|définitive|résumé)\b", r"\bil est (important|essentiel|crucial) de (noter|souligner)",
        r"\bjoue un rôle (clé|crucial|essentiel|central)", r"\bà l'ère (du|de la|des)\b", r"\bvéritable (levier|atout)",
        r"\bpierre angulaire\b", r"\bfaire la différence\b", r"\bsans plus attendre\b", r"\ben constante évolution\b",
        r"\bcrucial(e|es|aux)?\b", r"\brobuste(s)?\b", r"\blevier(s)?\b", r"\bincontournable(s)?\b", r"\bholistique(s)?\b",
        r"\bsynergie(s)?\b", r"\boptimiser (votre|vos|ton|tes)\b", r"\bdébloquer (le|votre|tout)\b", r"\brévolutionn(er|ant|aire)\b",
        r"\bpasser au niveau supérieur\b", r"\bexplorons\b", r"\bdécouvrons\b", r"\bfascinant(e|s|es)?\b",
    ],
    "en": [
        r"\bnot (just|only|merely)\b.*\bbut (also)?\b", r"\bit'?s not about\b", r"\bdelve\b", r"\btapestry\b", r"\btestament to\b",
        r"\bseamless(ly)?\b", r"\bin today'?s (fast-paced|digital|ever-changing)", r"\bever-evolving\b", r"\bunlock(ing)? the\b",
        r"\bgame[- ]changer\b", r"\bleverage\b", r"\brobust\b", r"\bcrucial\b", r"\bpivotal\b", r"\blandscape\b", r"\brealm\b",
        r"\bnavigate the\b", r"\bin conclusion\b", r"\bin summary\b", r"\bfeel free to\b", r"\bI hope this helps\b",
        r"\bgreat question\b", r"\blet'?s dive in\b", r"\bembark\b", r"\bfoster(ing)?\b", r"\bunderscore(s|d)?\b",
        r"\bshowcas(e|es|ing)\b", r"\bvibrant\b", r"\bmeticulous(ly)?\b", r"\belevate\b",
    ],
}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")

def detect_lang(text):
    fr = len(re.findall(r"\b(le|la|les|des|est|une|pour|avec|que|dans)\b", text, re.I))
    en = len(re.findall(r"\b(the|and|is|are|for|with|that|this|to)\b", text, re.I))
    return "fr" if fr >= en else "en"

def voice_bans(path):
    try:
        lines = open(path, encoding="utf-8").read().split("\n")
    except OSError:
        return []
    out, inside = [], False
    for l in lines:
        if l.startswith("## "):
            inside = "bann" in l.lower() or "banned" in l.lower()
            continue
        if inside and l.strip().startswith("-"):
            w = l.strip("- ").split("(")[0].strip().strip("«»\"' ")
            if w:
                out.append(r"\b" + re.escape(w) + r"\b")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--lang", default="auto")
    ap.add_argument("--voice", default=".claude/voice.md")
    ap.add_argument("--min-score", type=int, default=80)
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    lang = detect_lang(text) if a.lang == "auto" else a.lang
    lines = text.split("\n")
    findings, penalty = [], 0

    def add(n, kind, detail, cost):
        nonlocal penalty
        findings.append((n, kind, detail))
        penalty += cost

    patterns = PHRASES[lang] + voice_bans(a.voice)
    for i, l in enumerate(lines, 1):
        if re.search(r"\S\s*[—–]\s*\S", l) and not l.lstrip().startswith(("|", "-", "*")):
            add(i, "tiret", "tiret cadratin/demi-cadratin comme ponctuation", 6)
        for p in patterns:
            m = re.search(p, l, re.I)
            if m:
                add(i, "formule", m.group(0), 4)
        if EMOJI.search(l[:3]):
            add(i, "emoji", "emoji en début de ligne", 3)
        if lang == "fr" and re.search(r'"[^"]+"', l):
            add(i, "typo", 'guillemets droits "…" au lieu de « … »', 1)
        if lang == "fr" and re.search(r"\w[:;!?](\s|$)", l) and not re.search(r"https?:", l):
            add(i, "typo", "espace (insécable) manquante avant : ; ! ?", 1)

    words = len(re.findall(r"\w+", text))
    headers = sum(1 for l in lines if re.match(r"#{1,6} ", l))
    bullets = sum(1 for l in lines if re.match(r"\s*([-*•]|\d+\.) ", l))
    bold = len(re.findall(r"\*\*[^*]+\*\*", text))
    nonempty = [l for l in lines if l.strip()] or [""]
    if words < 400 and headers:
        add(0, "structure", f"{headers} titre(s) dans un texte court ({words} mots)", 5 * headers)
    if bullets / len(nonempty) > 0.5 and words > 60:
        add(0, "structure", f"{bullets}/{len(nonempty)} lignes en liste : préférer la prose", 8)
    if bold > max(2, words // 150):
        add(0, "structure", f"{bold} passages en gras : trop", 4)
    if text.count("!") > max(1, words // 200):
        add(0, "ton", f"{text.count('!')} points d'exclamation", 3)

    prose = re.sub(r"^\s*([-*•#|]|\d+\.).*$", "", text, flags=re.M)
    sents = [s for s in re.split(r"(?<=[.!?…])\s+", prose) if len(re.findall(r"\w+", s)) > 2]
    if len(sents) >= 6:
        lens = [len(re.findall(r"\w+", s)) for s in sents]
        mean, sd = statistics.mean(lens), statistics.pstdev(lens)
        if sd < 0.35 * mean:
            add(0, "rythme", f"phrases trop uniformes (moyenne {mean:.0f} mots, écart {sd:.1f})", 6)
        if mean > 28:
            add(0, "rythme", f"phrases longues (moyenne {mean:.0f} mots)", 4)

    score = max(0, 100 - penalty)
    print(f"score: {score}/100  langue: {lang}  mots: {words}")
    for n, kind, detail in findings:
        print(f"  {'L' + str(n) if n else 'global':>7}  [{kind}] {detail}")
    sys.exit(0 if score >= a.min_score else 1)

if __name__ == "__main__":
    main()