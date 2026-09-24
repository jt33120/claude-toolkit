# Paid ads — diagnostics and playbook

## Minimum data volumes before judging a metric

- CTR / CPC: at least ~1,000 impressions and a full week
- Conversion rate / CPA: at least ~30-50 conversions per campaign before treating a trend as real
- A single day or a weekend spike/dip is noise, not a trend — require a minimum of 7 days

## Diagnostic cutoffs (adjust to the business, these are starting points)

| Signal | Read |
|---|---|
| CPA rising 2+ consecutive weeks with flat/rising spend | saturation — targeting or creative fatigue, not a scaling opportunity |
| CTR dropping while frequency rises | creative fatigue — refresh, don't just add budget |
| High CTR, low conversion rate | landing page / offer mismatch, not a targeting problem |
| No conversion tracking configured | no verdict possible — fix tracking first |
| Cost per lead climbing while lead volume flat | targeting has narrowed or audience is exhausted |

## Change patterns and their approval-gate framing

- **Pause an underperformer**: state today's cost, cost after (EUR 0), leads/results lost, reversibility.
- **Shift budget between campaigns**: state absolute EUR moved, expected effect on the receiving campaign's CPA, and that the losing campaign's volume will drop proportionally.
- **Narrow/broaden targeting**: state expected reach change and CPA direction; this is a hypothesis, flag it as one, and set the metric to watch.
- **Refresh creative**: recommended every 2-4 weeks once frequency exceeds ~3-4x, before CTR visibly decays.
- **Publish a new ad**: highest-risk single action — it is public, under the brand, and spends immediately. Always its own gate, never bundled.

## Ad copy variants

Draft 3 variants, each testing exactly one variable: headline angle, offer framing, or CTA. Say explicitly what each variant tests, e.g. "Variant A tests a benefit-led headline; B tests a price-led headline; C tests urgency."

## Creative brief template

- Message: the one thing this ad must communicate
- Format: static / carousel / video, platform and size
- Text on image: exact copy, kept short
- CTA button text
- Reference: link to a similar ad that performed well, if any

## CSV export names by platform (what the founder sees in the UI)

- **Google Ads**: Reports → Predefined reports → Campaign performance, export CSV
- **Meta Ads Manager**: Ads Reporting → customize columns → Export → CSV
- **LinkedIn Campaign Manager**: Performance chart → Export
- **TikTok Ads Manager**: Reporting → Custom Report → Export
