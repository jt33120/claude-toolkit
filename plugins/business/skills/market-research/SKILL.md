---
name: market-research
description: "Research competitors and synthesize user/market research into a positioning brief, feature comparison, or set of prioritized findings. Triggers EN: competitive brief, competitive analysis, competitor research, synthesize research, market research, positioning gaps. Triggers FR: analyse concurrentielle, etude de marche, veille concurrentielle, synthese d'etudes utilisateurs, positionnement."
model: claude-opus-5-5
effort: medium
---

<!-- Provenance: merged and condensed from anthropics/knowledge-work-plugins (Apache-2.0) —
product-management/skills/competitive-brief, marketing/skills/competitive-brief, product-management/skills/synthesize-research.
Connector-specific boilerplate removed; tool-agnostic by default. -->

# Market Research

Two related jobs, run either or both: **(1) competitive brief** — research named competitors or a market
segment and produce a positioning/feature/messaging comparison; **(2) research synthesis** — turn interviews,
surveys, or feedback piles into ranked findings and recommendations. Route to whichever the user asked for;
a full go-to-market study runs both, brief first.

Any prose in the final deliverable goes through the core skills `writing-voice` and `language-strategy`.
Default business context: EUR pricing, GDPR/RGPD data-handling notes when personal data is discussed.

## Part 1 — Competitive brief

### Scope
Ask: which competitor(s) or feature area; focus (full comparison, pricing, positioning, GTM); what decision
this informs (strategy, sales battlecard, board material).

### Research
Use connectors when present (web search, CRM/deal notes for win-loss color, a knowledge base for prior
competitive docs); otherwise web search alone, or user-supplied notes. Sources: product/pricing pages, recent
launches and changelogs, press coverage, review sites (G2, Capterra, Trustpilot), job postings (strategic
signal), social/community discussion. Note the research date — competitive intel has a short shelf life.

### Brief structure
1. **Executive summary** — 2-3 sentences, biggest opportunity and biggest threat.
2. **Competitor profile(s)** — company overview, positioning (see `references/frameworks.md` for the
   positioning-statement template), recent momentum.
3. **Feature/messaging comparison matrix** — see `references/frameworks.md` for the rating scale and matrix template.
4. **Strengths and weaknesses** — evidence-based, do not dismiss or inflate.
5. **Opportunities** — unclaimed positioning, underserved segments, gaps in competitor content or product.
6. **Threats** — where they invest heavily, moves that could shift the market.
7. **Recommended actions** — 3-5 specific, prioritized (quick wins vs strategic moves).

Be honest about competitor strengths — a comparison that always wins is not credible. Weight by what matters
to buyers, not internal architecture or feature count.

### Optional add-ons (ask before producing)
- One-page executive summary
- Sales battlecard (`references/battlecard.md`)
- "How to win against X" guide
- A monitoring cadence: deep dive quarterly, scan monthly, alerts ongoing

## Part 2 — Research synthesis

### Gather
Accept any mix: pasted notes/transcripts, survey exports, support tickets, uploaded files, or connector pulls
(CRM notes, ticketing, analytics) when available. Ask: research type, number of sources/participants, the
question being investigated, what decision it feeds.

### Process each source
Extract observations, verbatim quotes (attribute by participant type — "enterprise admin", never a real name),
behaviors vs stated preferences, pain points, positive signals, context. Behavioral evidence outranks stated
preference.

### Synthesize
Apply thematic analysis (`references/synthesis-method.md`): familiarize, code, group into themes, check themes
against the data, refine, write up. Build a priority matrix (frequency x impact). Triangulate across sources
when possible — a finding backed by multiple methods is stronger than one from a single source; disagreement
between sources is signal, not noise, and gets reported honestly.

### Output — research synthesis
- **Overview** — methodology, question, timeframe.
- **Key findings** (5-8) — statement, evidence with source, frequency, impact, confidence (high/medium/low).
  Ordered by frequency x impact.
- **Segments/personas**, if the data supports distinct clusters — behavior-based, not demographic; 3-5 max.
- **Opportunity areas** — sized where possible: addressable users, frequency, severity (see
  `references/synthesis-method.md` for the sizing method and its caveats).
- **Recommendations** — specific and actionable, tied to findings.
- **Open questions** — genuine gaps, not answerable from context.

## Rules for both parts
- Every claim needs a source and a date; no bare numbers.
- Quotes are evidence, not the finding — the finding is the interpretation.
- Contradictions are interesting, not inconvenient; report them.
- 5-8 strong findings beat 20 weak ones. Resist over-synthesizing.
- Note the shelf life of the analysis (competitive: months; qualitative research: longer, but re-check when the
  market shifts).

## Output format
Tables for comparisons and scored findings. Clear headers, scannable. Ask after delivery whether to go deeper
on any section, create a battlecard, or draft a follow-up research plan.
