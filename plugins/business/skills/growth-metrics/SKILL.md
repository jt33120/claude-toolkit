---
name: growth-metrics
description: "Answers whether the SaaS growth engine is actually working: MRR/ARR, churn, activation, CAC, LTV, funnel conversion, channel and campaign return, product performance, and what customers say publicly and privately — ending in the top three actions worth taking this week. Also tracks brand health and review/reputation (ratings, themes, response drafts, quiet-customer win-back). Use for growth check, is my marketing working, SaaS metrics, MRR, churn, CAC, LTV, funnel, brand review, reviews, reputation, avis clients, réputation, indicateurs SaaS, taux de résiliation."
model: claude-opus-5-5
effort: medium
---

<!--
Provenance: merged and condensed from anthropics/knowledge-work-plugins (Apache-2.0):
small-business/skills/growth-pulse, marketing/skills/performance-report, marketing/skills/brand-review,
small-business/skills/review-reputation. Connector-specific boilerplate (HubSpot/Shopify/Mailchimp/
TikTok-native) generalized; kept tool-agnostic — runs from any connected source or pasted/exported data.
-->

# Growth Metrics

One page that answers whether the growth engine works, and what to do about it this week — the SaaS-metrics and reputation counterpart to a finance dashboard. Covers three linked jobs: the growth pulse (are we growing, and why), the performance report (channel/campaign detail when asked), and the reputation watch (public reviews + private churn signals).

## Step 1 — Pull everything available, in one pass

Use whatever is connected or was exported/pasted: subscription/billing data (MRR, new/expansion/contraction/churned revenue), product analytics (activation, active users), CRM/pipeline (leads, conversion by stage), ad platforms (spend and result by campaign), public reviews. **Zero connectors is a supported path** — ask for exports (billing export, a pipeline export, an ads CSV) and build the same pulse from files; say so plainly rather than stalling.

## Step 2 — Compute the core SaaS metrics

See `references/metrics-benchmarks.md` for definitions and formulas. At minimum, when data allows:

- **MRR/ARR** and month-over-month growth rate
- **Churn** — logo churn and revenue churn (gross and net, separately)
- **Activation rate** — % of new signups reaching the defined "aha" action
- **CAC** — fully loaded (marketing + sales spend) ÷ new customers
- **LTV** and LTV:CAC ratio
- **Funnel conversion** — visitor → signup → activated → paying, with the biggest drop-off named
- **Channel/campaign return** — spend vs. attributed revenue, cost per lead/customer per channel

A metric with no data gets marked "n/a," never silently dropped.

## Step 3 — Find the story, not just the numbers

Connect the views rather than listing them:
- Spend rising while CAC rises = channel saturating, not scaling
- Strong signups with falling activation = onboarding problem, not a marketing problem
- One channel or one customer segment carrying the whole trend = growth is more fragile than the total suggests
- Sentiment (reviews) dropping while MRR holds = early warning that shows up in churn next
- Net revenue churn above 5-7%/month for early-stage SaaS is a red flag worth naming explicitly

## Step 4 — Reviews and reputation (on request, or when relevant to churn)

Gather public reviews (G2, Capterra, Trustpilot, app stores) and any support/complaint signal. Group into 3-5 themes with verbatim quotes (never paraphrase — the exact wording is the evidence) and a signal count each. Draft a reply to every review needing one, through **writing-voice**/**language-strategy**, under ~60 words, specific and non-defensive; nothing posts without explicit approval. Flag customers who have gone quiet relative to their own normal rhythm (not an industry average) and draft a win-back message per customer, referencing something real — never invent a discount the founder hasn't approved.

## Step 5 — Three actions, ranked

Every run ends in exactly three actions (or fewer, if the honest answer is "nothing needs to change" — say that instead of manufacturing filler). Each action: what to do, why (the number that justifies it), and its rough size (opportunity or risk in EUR or %).

## Output

Numbers lead, words follow: "paid social drove 41 signups at EUR 18 CAC, down from EUR 31 last month" — never "paid social performed well." Every number carries its comparison period. Name the specific channel/campaign/customer, never "some campaigns underperformed."

## What not to do

- Never invent attribution — if a channel's contribution can't be traced, say so.
- Never report CRM pipeline value as realized revenue — label which is which.
- Never double-count revenue across sources (e.g. a Stripe charge also appearing in a billing export).
- Never post a review reply or send a win-back message without approval.
- Never fabricate a review count, rating average, or churn number not actually in the data.

## Reference files

- `references/metrics-benchmarks.md` — SaaS metric formulas, benchmark ranges, funnel/attribution guidance, review-response patterns, quiet-customer thresholds.
