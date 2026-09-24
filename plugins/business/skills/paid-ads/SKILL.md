---
name: paid-ads
description: "Reads paid-ad performance across Google, Meta, LinkedIn and TikTok Ads (via connector or exported CSV), explains in plain terms what's working and what's burning budget, recommends targeting/budget/creative changes with the exact EUR impact of each, drafts new ad copy and creative briefs, and only executes a change in the ad account after explicit approval. Use for ad performance, ROI on ads, cost per lead going up, should I pause this campaign, write ad copy, Google Ads, Meta Ads, LinkedIn Ads, TikTok Ads, publicités payantes, performance des annonces, budget pub, coût par lead."
model: claude-opus-5-5
effort: medium
---

<!--
Provenance: merged and condensed from anthropics/knowledge-work-plugins (Apache-2.0):
small-business/skills/ad-manager.
Connector-specific (TikTok-native, Canva, Zapier build-connector) boilerplate generalized to
"whatever ad platform is connected or exported" and made tool-agnostic.
-->

# Paid Ads

Turns ad spend into a decision the founder can make in two minutes, then makes the approved change. Never touches an ad account without an explicit yes on that specific change.

## Step 1 — Get the performance data

Use whatever is connected (Google Ads, Meta, LinkedIn, TikTok Ads, or any other platform via a connector). **The CSV export path is the main road, not a fallback** — most small teams start here. Ask for the export by the name they'll see in the interface: "export the last 30 days as CSV, broken down by campaign." Say once which mode is running (connector or CSV) and never stall waiting on a connector.

Pull, when available: CRM/analytics data on what actually closed (signups, paid conversions), so platform-reported results can be checked against real outcomes.

## Step 2 — Read the account honestly

Work top-down: account → campaign → ad group → creative. Most small accounts have one or two campaigns carrying everything and a long tail quietly eating budget. For every campaign establish: cost, result, cost per result, and trend (improving or decaying). A campaign with no conversion tracking has no verdict — say tracking is missing rather than judging on clicks.

## Step 3 — Tell the truth about attribution

The platform and the CRM/analytics will disagree — always. Report both, name the gap in one sentence (platforms count view-through/cross-device; the CRM misses untracked sources), and give the number to actually steer by (usually cost per paid signup/customer from the CRM, platform figure shown as the optimistic bound). Never blend the two into a single fabricated ROI number.

## Step 4 — Recommend changes with EUR attached

Every recommendation carries: what to change (specific campaign/ad set/ad by name), why (the number that justifies it), EUR impact (absolute monthly change, never a bare percentage — "cut retargeting 30%, from EUR 1,200 to EUR 840/month"), and what to watch to know within a week if it worked. Rank by impact, not ease. See `references/ad-playbook.md` for the common change patterns (budget shifts, pausing saturated channels, targeting fixes, creative refresh cadence).

## Step 5 — Draft copy and creative briefs

Route all ad copy through **writing-voice** and **language-strategy** before finalizing — get tone and EN/FR language mix right for the target market. Draft 3 variants per ad, each testing one distinct thing (not three near-identical headlines). For visuals, write a creative brief (message, format, sizes, on-image text) — a founder without a design tool can hand this to a freelancer or Canva.

## Step 6 — Execute, one approval at a time

Every executed change gets its own approval gate, stating the EUR impact first:

```
Change:      Pause "Retargeting — Broad" campaign
Costs today: EUR 1,400/month
After:       EUR 0/month
Net:         Saves EUR 1,400/month, stops ~12 leads/month
Reversible:  Yes, restart any time
Proceed?
```

A yes covers exactly that one change. Never bundle several changes behind one approval. In CSV mode, produce the same block as click-by-click instructions instead of executing directly.

## Step 7 — Close the loop

Set a check-back date and say what would make the change a mistake — a change nobody revisits is a guess, not a decision.

## What not to do

- Never execute anything without a fresh, explicit yes for that specific change.
- Never express budget change as a percentage alone — always the absolute EUR.
- Never present a single blended ROI figure as fact.
- Never judge a campaign with no conversion tracking.
- Never recommend more spend on a channel whose cost per result is climbing (that's saturation, not scale).
- Never read a few days of data as a trend — see `references/ad-playbook.md` for minimum volumes.

## Reference files

- `references/ad-playbook.md` — metric cutoffs, minimum data volumes, change patterns and their EUR-impact framing, ad-copy variant guidance.
