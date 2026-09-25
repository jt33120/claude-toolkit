---
name: writing-voice
description: "Write or rewrite any text (email, LinkedIn post, landing page, UI microcopy, client report, README, message) in the project's own voice and without AI tells: builds a per-project voice profile interactively, adapts the format to the medium, checks the draft with a deterministic script, and learns from the user's edits. Use for any text meant for humans. FR : « écris un mail », « rédige un post », « réécris ce texte », « ça fait trop IA », « quel ton », « texte de la landing », « microcopy »."
---

# Writing voice

## 1. Load the voice

Read `.claude/voice.md` (Cowork: the project's voice doc). If missing, build it with the user before writing, in one short exchange:

- Audience and relationship, **tu ou vous**
- Sliders 1–5: formel ↔ familier · concis ↔ détaillé · neutre ↔ engagé · technique ↔ accessible · chaleureux ↔ sec
- 2–3 texts they like (or existing ones: site, past emails) — infer the voice from them and ask to confirm
- Words and phrasings to ban / to keep

Write it with `templates/voice.md`. Never impose a voice: propose, the user confirms.

## 2. Match the medium

| Medium | Format |
|---|---|
| Email, message, Slack | Prose, no headings, no bold, 3–8 short paragraphs max, one clear ask |
| LinkedIn / social | Short lines, one idea, concrete example, no hashtag pile, no emoji bullets |
| Landing / marketing | Benefit-led headline, short sections, specific proof over adjectives |
| UI microcopy | Verbs, ≤ 7 words for buttons/labels, say what happens, same term everywhere |
| Report, docs, README | Headings only if > ~400 words, lists only for real enumerations |

Default to prose. Lists and headings must earn their place.

## 3. Write, then check

1. Draft in the voice.
2. Run `python3 scripts/ai_tells.py <file|-> --voice .claude/voice.md` (FR and EN: dashes used as punctuation, stock phrases, emoji bullets, heading/list/bold density, uniform sentence rhythm, French typography).
3. Rewrite until the score is ≥ 80, then re-read against `references/ai-tells.md` for the structural tells a script cannot see.
4. If the `humanizer` skill (blader/humanizer) is installed, use it as a final pass for English text.

Do not mention the check to the reader; deliver only the text (plus alternatives if asked).

## 4. Learn from edits

When the user edits a draft, compare versions and append the rules you can infer to `## Règles apprises` in `voice.md` (e.g. « phrases plus courtes », « jamais "par ailleurs" », « tutoiement »). Tell the user in one line what was added.