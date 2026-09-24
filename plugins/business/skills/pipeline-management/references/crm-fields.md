# Pipeline management — flags, scoring, and spreadsheet-CRM structure

## Pipeline risk flags

| Flag | Condition |
|---|---|
| Stale | no activity in 14+ days (tune to the sales cycle length) |
| Slipping | close date in the past, or moved out 2+ times |
| Blank next step | no next action recorded |
| Stuck | in current stage 2x longer than that stage's median |
| Single-threaded | only one contact with recorded activity |

## Signal-adjusted win probability

Start from the CRM's own stage-default probability, then adjust:

| Signal | Adjustment |
|---|---|
| Champion actively engaged (recent email/meeting) | +10% |
| Multi-threaded (3+ contacts with activity) | +5% |
| Exec sponsor identified and met | +10% |
| Mutual action plan agreed | +10% |
| No activity 14+ days | −10% |
| Champion gone quiet 14+ days | −15% |
| New stakeholder introduced late | −5% |
| Competitor actively in deal | −10% |
| Close date slipped 2+ times | −10% |
| Single-threaded | −10% |
| Open pricing gap (evidenced) | −10% |

Floor 5%, ceiling 95%. Show the math explicitly rather than presenting a bare number.

## CRM hygiene checks

| Check | Flag if |
|---|---|
| Amount | blank or 0 |
| Close date | past, or unchanged since creation on a 30+ day-old deal |
| Next step | blank or unchanged 14+ days |
| Stage age | in current stage >2x median |
| Activity | none in 14+ days |
| Contacts | none, or only one associated |
| Stage criteria | exit criteria not evidenced (e.g. "Proposal" stage, no proposal doc found) |

## Coverage heuristic

Weighted open pipeline should be roughly 3x the remaining quota gap for the period. Note explicitly when under, and by how much.

## Lightweight spreadsheet CRM (when there is no CRM tool)

Four tabs, minimum viable:

- **Contacts** — name, company, email, role, source
- **Deals** — contact, deal name, stage, amount, close date, next step, last activity date
- **Activity Log** — date, contact/deal, type (call/email/meeting), summary
- **Next-Step Queue** — deal, owner, action, due date

Maintain it exactly like a real CRM: propose changes, apply on approval, never silently overwrite. It exports cleanly if the team later adopts a dedicated CRM tool.

## Lead-scoring dimensions (for triage)

- **Engagement** — replies, opens, site visits (recent window, e.g. last 30 days)
- **Company fit** — against the stated ICP (industry, size); default conservatively if no ICP given
- **Urgency** — lead age, explicit urgency language ("ASAP," "deadline," "budget approved")
- **Recency penalty** — subtract if already touched very recently (avoids re-flagging same-day contacts)

If the score spread across the list is narrow (<~10 points top to bottom), say the signal is too flat to rank meaningfully and order by CRM facts (e.g. lead age) instead.
