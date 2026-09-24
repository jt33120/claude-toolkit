# Growth metrics — formulas, benchmarks, and patterns

## Core SaaS metric formulas

| Metric | Formula | Notes |
|---|---|---|
| MRR | sum of active monthly recurring revenue | annualize x12 for ARR |
| MRR growth rate | (MRR this month − MRR last month) / MRR last month | |
| Logo churn | customers lost / customers at period start | |
| Gross revenue churn | MRR lost from cancellations+downgrades / MRR at period start | expansion excluded |
| Net revenue churn | (MRR lost − MRR gained from expansion) / MRR at period start | can be negative (good) with strong expansion |
| CAC | (sales + marketing spend) / new customers acquired | fully loaded, same period |
| LTV | (avg revenue per account × gross margin %) / churn rate | simplified; use cohort data if available |
| LTV:CAC | LTV / CAC | 3:1 is a common healthy target; below 1:1 is unsustainable |
| CAC payback | CAC / (avg monthly revenue per account × gross margin %) | months to recover CAC |
| Activation rate | users reaching the "aha" action / new signups | define the aha action per product |

## Early-stage SaaS benchmark ranges (directional, not gospel)

- Net revenue churn: negative to 2%/month is strong; 5%+ is a red flag worth digging into.
- Logo churn: under 3-5%/month for SMB-targeted SaaS is reasonable; enterprise should be much lower.
- LTV:CAC: 3:1 is the classic target; under 1:1 means each customer costs more than they're worth.
- CAC payback: under 12 months is healthy for bootstrapped/early-stage; 12-18 acceptable with runway.
- Trial-to-paid or free-to-paid conversion: highly product-dependent — track your own trend over absolute benchmark.

## Funnel stages to track

Visitor → Signup → Activated (aha action) → Paying → Retained (past first renewal) → Expanded. Compute the conversion rate between each step and name the largest drop-off — that is usually worth more attention than a new acquisition channel.

## Attribution guidance

- Start with last-touch if nothing else exists — simplest and actionable.
- Compare first-touch vs. last-touch to see which channels drive awareness vs. conversion; awareness channels always look weak in last-touch models.
- No model is perfect; use directionally, never as absolute truth. Self-reported "how did you hear about us" is useful qualitative color, unreliable as quantitative data.

## Review response patterns (≤60 words each)

- **Negative**: name the specific thing that went wrong, say what changed, move the rest offline with a real contact route. No "sorry you feel that way," no policy-defending.
- **Positive**: short, specific, thank them for the actual thing mentioned.
- **Mixed**: acknowledge both halves honestly.
- **Unfair/false**: correct the factual point once, calmly, then stop.

## Quiet-customer / churn-risk signal

A "quiet" customer is one whose gap since last activity/order has stretched past *their own* normal rhythm, not an industry average — a monthly-active customer silent for 2 months is a stronger signal than an annual-plan customer silent for 2 months. Rank win-back candidates by relationship value, not by silence length alone. A negative review followed by no further activity is the clearest combined churn signal — flag it for a personal outreach, not just an automated message.
