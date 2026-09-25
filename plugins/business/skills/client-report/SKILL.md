---
name: client-report
description: "Writes factual, anonymized status reports and stakeholder/Codir-style synthesis notes: progress, KPIs, risks, decisions needed, in neutral professional French or English. Triggers EN: status report, stakeholder update, executive summary, synthesis note, board memo. Triggers FR: note de synthese, rapport d'avancement, note Codir, compte-rendu de mission, note preparatoire."
---

<!-- Provenance: merged from anthropics/knowledge-work-plugins (Apache-2.0) — product-management/skills/stakeholder-update,
operations/skills/status-report — and the author's private skill "redaction-synthese" (factual/anonymization style rules,
unreleased). All names, client codes and colors below are fictional examples, not real client or personal data. -->

# Client Report

Produce a status report or a synthesis/board note: factual, anonymized, professional. Two audiences drive
structure — a **status report** (progress/KPIs/risks/decisions, any cadence) or a **synthesis note** (a fuller
Codir/board-style memo with context, options and a business case). Route by what's asked; a synthesis note
subsumes a status report's sections. All prose is written directly to this skill's style rules below, then
still passes through `writing-voice` and `language-strategy` for final polish. Default context: France — dates
as "mois AAAA", amounts in EUR/k€, RGPD note if the report handles personal data.

## Step 1 — Determine audience and cadence
Ask: audience (executives/board — high-level and brief; a working team — more technical detail and links;
external/client — no internal jargon), cadence (weekly/monthly/ad hoc/launch), and what decision or action
this update should drive.

## Step 2 — Gather inputs
Use whatever is connected (project tracker, chat, calendar) or ask the user directly for: what was
accomplished, current blockers/risks, decisions made or needed, what's next. List every source used (mails,
docs, exchanges) before drafting, and flag names that need anonymizing (Step 4).

## Step 3 — Structure

**Status report** (short form):
```
Status: Vert / Jaune / Rouge   (reflect reality, not optimism — yellow flagged early is good risk management)
TL;DR: [one sentence]
Progres: [outcomes tied to goals, dated]
Risques: [risk -> mitigation -> ask if any]
Decisions requises: [decision -> options + recommendation -> deadline]
Prochaines priorites: [1-3 items]
```

**Synthesis note** (Codir/board form), adapt length to context:
1. Page de garde — title, destinataires par fonction, date, version, mention de confidentialite si besoin.
2. Synthese executive — constat (3-5 lignes), recommandation (3-5 lignes), chiffrage condense (1 tableau),
   decisions a prendre (max 5).
3. Contexte — etat actuel, atouts et contraintes (tableau).
4. Analyse / options — criteres (tableau), revue par option, recap score.
5. Recommandation et plan — option retenue, roadmap (tableau par phase), business case (tableau financier).
6. Risques et mitigations — tableau Risque / Probabilite / Impact / Mitigation.
7. Decisions a valider — tableau # / Decision / Owner (par fonction) / Deadline.
8. Annexes — hypotheses de chiffrage, glossaire, sources.

## Step 4 — Style rules (mandatory, check before delivery)

**No personal names in the body.** Refer by function only ("le COO", "la direction produit", "le lead
backend", "l'equipe frontend"), never by first or last name. Exception: a cover-page author/recipient line,
and even there prefer the function. Example:

| Avoid | Use |
|---|---|
| "Alice a valide l'option B le 14 avril" | "La direction generale a valide l'option retenue mi-avril" |
| "Marc (lead backend) recommande..." | "Le lead backend recommande..." |

**No em/en dashes** (— or –) as sentence connectors — replace with a comma, a period, a semicolon, or
parentheses for an aside, and a colon to introduce a list or explanation.

**No judgment on the past or on people.** State facts and recommendations, not verdicts on prior decisions.

| Avoid | Use |
|---|---|
| "Le debat tourne en rond depuis 2023" | "Le sujet est a l'ordre du jour depuis 2023 et n'a pas encore ete tranche" |
| "L'option D est dominee par E" | "Sur l'ensemble des criteres evalues, l'option E obtient un meilleur score (34/40 contre 28/40)" |

**No AI-sounding connectors or superlatives.** Avoid "en outre", "il est important de noter que", "en somme",
"cela dit" as filler, and "absolument crucial" / "totalement incontournable" — use neutral equivalents
("determinant", "necessaire").

**Tables over prose enumeration.** Any 3+ item list with sub-attributes (name + criterion + value) becomes a
table, not a numbered paragraph. Key recommendations or the executive synthesis get a visually distinct callout
box, not buried in running text.

**One bullet level.** No nested lists — use sub-tables or sub-headers for hierarchy.

## Step 5 — Checklist before delivery
No personal names in the body; no em/en dashes; no judgment language; no AI-sounding connectors or
superlatives; every 3+ item enumeration is a table; the recommendation is visually distinct; units and date
formats are consistent (EUR, k€, "Mois AAAA"); a decisions-recap table closes the document; cover page and
footer (document name, month, page number) present for a synthesis note.

## Output
Deliver as the requested format (markdown, DOCX if the user wants formatted pagination). Ask once whether
tone, length, or emphasis needs adjusting before finalizing.
