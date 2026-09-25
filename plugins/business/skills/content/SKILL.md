---
name: content
description: "Plans and drafts marketing content end to end for a small SaaS team: a rolling editorial calendar, on-brand LinkedIn/blog/newsletter/social copy, and full launch-campaign briefs (objective, audience, message, channel, calendar, budget, metrics). Use for content strategy, editorial calendar, blog post, LinkedIn post, newsletter, SaaS product launch, campaign plan, content marketing, calendrier éditorial, plan de contenu, campagne de lancement, article de blog, post LinkedIn, newsletter, contenu marketing."
---

<!--
Provenance: merged and condensed from anthropics/knowledge-work-plugins (Apache-2.0):
marketing/skills/content-creation, marketing/skills/draft-content, marketing/skills/campaign-plan,
small-business/skills/social-content-engine, small-business/skills/content-strategy.
Connector-specific (Canva/HubSpot/Shopify/Mailchimp) boilerplate removed; kept tool-agnostic.
-->

# Content

Turns a growth goal into a running content operation: what to say, where, on what cadence, and — for a launch — the full campaign brief around it. Built for a solo founder or a 2-5 person team who cannot afford a dedicated content person yet.

All customer-facing copy this skill drafts must go through the core skills **writing-voice** (tone/voice consistency) and **language-strategy** (which language(s) to write in, EN/FR mix). Load and apply them before drafting; do not invent a voice.

## When to run which mode

1. **Strategy** — "what should I post/promote this month?" Look at what is actually selling or getting signups (exports from Stripe/analytics, or a pasted summary) and produce a 30-day brief: push hard / hold steady / reposition, with the reasoning. 200-400 words, no calendar yet.
2. **Calendar** — turn an approved strategy (or a bare request) into a rolling editorial calendar: date, channel, topic, status. Hold it between runs — extend the horizon, do not rebuild it from scratch each time.
3. **Draft** — write one piece: blog post, LinkedIn/X/Instagram post, newsletter, landing page copy, press release, case study, or a SaaS launch announcement. See `references/content-templates.md` for structure by type.
4. **Campaign** — a full launch or push: objective, audience, key messages, channel mix, week-by-week calendar, content pieces needed, budget split, success metrics, risks. See `references/content-templates.md` for the campaign brief structure and channel/budget benchmarks.

## Step 1 — Ground the ask

Ask only what is missing and needed to proceed: topic/goal, audience (who is this SaaS feature or offer for), one to three key messages, tone (or rely on writing-voice), and length/format constraints. Do not block on connectors — pasted numbers, a rough sales summary, or "just draft it" are all complete inputs.

## Step 2 — Draft

Follow `references/content-templates.md` for the shape of each content type (hook, structure, CTA) and headline/hook formulas. Every piece gets:
- 2-3 headline/subject-line options
- A hook in the first line/paragraph
- One clear CTA (never more than one primary ask)
- Channel-appropriate length and format (LinkedIn ≠ X ≠ newsletter ≠ blog)

For SEO-facing content (blog, landing pages), suggest one primary + 2-3 secondary keywords and note title/meta/H1 placement — for a full audit, hand off to `seo-visibility`.

## Step 3 — Calendar and cadence

Default cadence for a small team (adjust to their bandwidth): 1 blog post every 1-2 weeks, 3-5 social posts/week across one or two channels (do not force every channel), one newsletter every 1-2 weeks. Batch by weekly theme; leave ~20% of slots open for reactive content. Present as a table: Date | Channel | Topic/Piece | Status.

## Step 4 — Campaign brief (launches only)

When the ask is a product launch or a real push (not routine posting), build the full brief per `references/content-templates.md`: objective (SMART, one sentence), audience, key messages with proof points, channel selection with effort/budget notes, week-by-week content calendar with dependencies, content pieces needed (must-have vs nice-to-have), budget split if given, 2-3 risks with mitigations, and success metrics tied to the objective.

## Step 5 — RGPD / EU context

Default to EUR pricing mentions and French/EU norms unless told otherwise. Any newsletter or email content must reference consent/opt-in and an unsubscribe path; any landing page or ad copy mentioning cookies/tracking should flag that a cookie-consent banner is required under RGPD — note it, do not draft legal text (hand to `legal-check` for the actual compliance review).

## Output

Present drafts and the calendar inline, clearly formatted, ready to paste. Never invent metrics, pricing, discounts, or customer numbers that were not given. After delivering, ask if they want a variation for another channel, a revision, or the calendar extended.

## What not to do

- Never fabricate stats, testimonials, or "X customers already use this."
- Never publish or schedule anything — this skill drafts; the founder posts.
- Never guess brand voice — use writing-voice, or ask for 2-3 samples.

## Reference files

- `references/content-templates.md` — structure by content type, headline/hook formulas, campaign brief structure, channel and budget benchmarks, cadence guidance.
