---
name: process-mapping
description: "Documents a business process (steps, RACI, SOP) and analyzes it for automation opportunities with AI/n8n/scripts, with a before/after comparison and an ROI estimate. Triggers EN: document this process, write an SOP, this process is slow, streamline this workflow, automate this, where's the bottleneck. Triggers FR: documenter un processus, ecrire une procedure, ce processus est trop lent, automatiser cette tache, ou est le goulot d'etranglement."
---

<!-- Provenance: merged and condensed from anthropics/knowledge-work-plugins (Apache-2.0) —
operations/skills/process-doc, operations/skills/process-optimization. Automation-opportunity step extended
with concrete AI/n8n/scripting framing per this plugin's context. -->

# Process Mapping

Document a process as an SOP, then find where it can be automated. Run documentation alone when that's all
that's asked; run both when the goal is improvement, since you can't size automation opportunities on a
process nobody has mapped yet. All prose goes through `writing-voice` and `language-strategy`.

## Part 1 — Document the process (SOP)

Take the process in whatever form it arrives: a walkthrough, pasted existing docs, or just a name to ask
about. Start messy — an imperfect description in, a structured SOP out.

Produce:
```
Process: [name]
Owner: [role]  |  Last updated: [date]  |  Review cadence: [quarterly/annually]

Purpose: [why this process exists]
Scope: [included / excluded]

RACI
| Step | Responsible | Accountable | Consulted | Informed |

Process flow: [step-by-step or simple text flowchart]

Detailed steps (per step): Who | When (trigger) | How | Output

Exceptions and edge cases
| Scenario | What to do |

Metrics
| Metric | Target | How measured |
```

**Include the exceptions.** "Usually we do X, but sometimes Y" is the most valuable part to capture — it's
what a written procedure normally loses. Name who does what today even if roles will change; it's what makes
the next step (automation) concrete rather than abstract.

## Part 2 — Find automation opportunities

### Step 1 — Map current state
For every step already documented in Part 1: who does it, how long it actually takes (not the target — the
real time, including waiting), what's manual, what requires an approval.

### Step 2 — Identify waste
- **Waiting** — time in queues or waiting for an approval/handoff.
- **Rework** — steps that fail and get redone.
- **Handoffs** — each one is a potential delay or failure point; count them.
- **Over-processing** — steps that add no value to the outcome.
- **Manual work** — anything a human does that a system could do as reliably.

### Step 3 — Design the future state
For each waste point, name the concrete fix and its mechanism, not just "automate it":
- **AI-assisted step** — an LLM drafts, classifies, extracts, or summarizes; a human still approves the
  output. Good fit when the task is judgment-adjacent (triage, drafting, extraction) rather than pure
  data-shuffling.
- **Workflow automation (e.g. n8n)** — deterministic, rule-based steps: trigger → transform → route, with no
  judgment call. Good fit for connecting two systems, scheduled pulls, notification routing, data
  reconciliation.
- **Script/one-off tool** — a repeated manual data transformation with a stable input/output shape.
- **Eliminate** — some steps survive only because "that's how it's always been done"; check whether the step
  still serves its stated purpose before automating it.

Reduce handoffs, parallelize independent steps, and replace approval gates with checkpoints (visibility
without blocking) wherever the risk profile allows it.

### Step 4 — Estimate ROI
For each proposed change: time saved per cycle x cycles per month = hours/month recovered; a rough build/setup
cost (hours or a tool's EUR/month cost); payback period in months. Be honest about what stays manual — not
everything should be automated, and say so when a step is judgment-heavy, low-frequency, or high-stakes enough
that automation risk outweighs the time saved.

### Output — before/after comparison
```
Step | Current (who, time) | Proposed (mechanism) | Time saved/cycle | Setup effort | Payback
```
Plus a short implementation plan ordered by ROI: quick wins first (low effort, clear payback), then anything
needing a build.

## Rules
- Never propose automating a step you haven't seen the actual current-state time/frequency for — ask rather
  than assume.
- Name the mechanism (AI draft + human approval / n8n workflow / script / elimination), not just "automate".
- Flag any step handling personal data (RGPD) before proposing it move to an automated or AI-assisted path —
  note the data involved and whether a human review gate is still needed for compliance.
