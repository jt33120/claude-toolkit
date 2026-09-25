---
name: language-strategy
description: "Juggle French and English efficiently: English as the working language for prompts, specs, code and AI-to-AI briefs (models perform best in English), the audience's language for deliverables, with a per-project glossary and native rewriting instead of literal translation. Use when a task mixes FR and EN, when writing specs or prompts for other AIs, when translating or producing bilingual content, or when setting up BMAD languages. FR : « en anglais ou en français », « traduis », « version anglaise », « bilingue », « quelle langue pour la spec »."
---

# Language strategy

**Principle:** English to *work*, the audience's language to *deliver*. The user can always talk in French; Claude does the switching, not the user.

## 1. Which language for what

| Artifact | Default | Why |
|---|---|---|
| Conversation with the user | The user's language (French) | Comfort, precision of intent |
| Internal briefs: subagent prompts, plans, task lists | English | Best model performance, fewer tokens |
| Specs, PRD, architecture, stories (BMAD) | English, unless the client reads them | Same, and reusable by any tool |
| Code, identifiers, comments, commits, PRs | English | Industry convention |
| Prompts for other AIs (Codex images, other agents) | English | Same |
| Client-facing deliverables, UI copy, marketing, emails | The audience's language | It is the product |

BMAD: set `communication_language: French` and `document_output_language: English` (or French for client-facing docs) in the BMAD config.

## 2. Translate intent, not words

When the user gives a complex technical request in French, silently convert it into a precise English working brief (keep proper nouns and French business terms that have no exact equivalent, with a gloss). Do not ask the user to switch language.

Remind the user **at most once per session, in one line,** only when it matters: a long prompt they are about to paste into another AI tool, or a spec others will build from — « Astuce : pour ce prompt, l'anglais donnera de meilleurs résultats, je te le fournis en anglais. » Then provide it.

## 3. Bilingual deliverables

- Write each language **natively from the same brief** (transcreation), not a line-by-line translation.
- Localize: dates, numbers, currency, units, tu/vous, French typography (« », espaces insécables), idioms.
- Keep the per-project glossary `.claude/glossary.md` (term FR | term EN | note) so the same concept always gets the same word. Terms French tech people say in English (déployer, commit, pull request, backlog) stay as used.
- Run `writing-voice` (and its `ai_tells.py` check) on **each** language version. `voice.md` may hold a section per language.
