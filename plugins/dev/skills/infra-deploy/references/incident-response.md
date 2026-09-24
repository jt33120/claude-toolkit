# Incident Response

Manage an incident from detection through postmortem, for a Vercel + Railway +
Supabase/Neon stack.

## Modes

```
new [description]     # Start a new incident
update [status]       # Post a status update
postmortem            # Generate postmortem from incident data
```

If it's unclear which phase the incident is in, ask.

## How It Works

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    INCIDENT RESPONSE                               │
├──────────────────────────────────────────────────────────────────────────┤
│  Phase 1: TRIAGE                                                  │
│  ✓ Assess severity (SEV1-4)                                     │
│  ✓ Identify affected systems (Vercel frontend? Railway service?  │
│    Supabase/Neon database?) and users                            │
│  ✓ Assign roles (incident lead, comms, responders)                │
│                                                                    │
│  Phase 2: COMMUNICATE                                              │
│  ✓ Draft internal status update                                  │
│  ✓ Draft user-facing communication (if needed)                  │
│  ✓ Set up a shared channel/thread and update cadence              │
│                                                                    │
│  Phase 3: MITIGATE                                                 │
│  ✓ Document mitigation steps taken                               │
│  ✓ Track timeline of events                                      │
│  ✓ Confirm resolution                                            │
│                                                                    │
│  Phase 4: POSTMORTEM                                               │
│  ✓ Blameless postmortem document                                 │
│  ✓ Timeline reconstruction                                       │
│  ✓ Root cause analysis (5 whys)                                  │
│  ✓ Action items with owners                                      │
└───────────────────────────────────────────────────────────────────────────┘
```

## Severity Classification

| Level | Criteria | Response Time |
|-------|----------|---------------|
| SEV1 | Service down, all users affected | Immediate, all-hands |
| SEV2 | Major feature degraded, many users affected | Within 15 min |
| SEV3 | Minor feature issue, some users affected | Within 1 hour |
| SEV4 | Cosmetic or low-impact issue | Next business day |

## Phase 1: Triage — Where to Look on This Stack

Pull signal before guessing at cause:
- **Vercel**: build failing? Check the latest deployment's build/runtime logs (Vercel MCP
  connector, or `vercel logs` / `vercel inspect`). A bad deploy is the single most common
  "suddenly everything is broken."
- **Railway**: service crash-looping or erroring? Check deploy status and logs (Railway MCP
  connector, or `railway logs`), and metrics (error rate, latency, memory) if tracing is set
  up.
- **Supabase**: database errors, RLS denials, connection exhaustion? Check the Supabase MCP
  connector's logs/advisors, or the dashboard's logs explorer.
- **Neon**: is this against a Neon-branched database (e.g. a preview branch someone pointed
  prod traffic at by mistake)? Check branch status and the default branch.
- **GitHub Actions**: did a just-merged PR's deploy trigger this? Check the most recent
  workflow run and what it deployed.

Identify: which layer failed, what changed right before it broke (a deploy, a migration, a
traffic spike, an upstream dependency), and how many users are affected.

## Phase 2: Communicate

Provide clear, factual updates at a regular cadence. Include: what's happening, who's
affected, what we're doing, when the next update is.

### Output — Status Update

```markdown
## Incident Update: [Title]
**Severity:** SEV[1-4] | **Status:** Investigating | Identified | Monitoring | Resolved
**Impact:** [Who/what is affected — e.g. "Vercel frontend 500s for all users" or
             "Railway worker queue backing up, delayed emails"]
**Last Updated:** [Timestamp]

### Current Status
[What we know now]

### Actions Taken
- [Action 1]
- [Action 2]

### Next Steps
- [What's happening next and ETA]

### Timeline
| Time | Event |
|------|-------|
| [HH:MM] | [Event] |
```

## Phase 3: Mitigate

Stabilize first — this is not the time for `systematic-debugging`'s root-cause process.
Common mitigations on this stack, roughly fastest-to-slowest:
1. **Rollback the deploy.** Vercel: promote the previous deployment. Railway: redeploy the
   previous build. This is almost always the fastest path to stopping the bleeding if the
   incident started right after a deploy.
2. **Kill switch a feature flag**, if the incident traces to a specific feature.
3. **Scale up** the Railway service if it's a load/capacity issue, or check Supabase
   connection pooling limits if it's a database connection exhaustion issue.
4. **Point traffic away from a bad Neon branch** back to the correct one, if a branch mixup
   caused this.
5. Only once users are unaffected: hand off to `systematic-debugging` to find the actual
   root cause before writing the permanent fix.

Document each mitigation step taken and the timeline as you go — this becomes the postmortem
timeline later, and reconstructing it from memory afterward loses detail.

## Phase 4: Postmortem

### Output — Postmortem

```markdown
## Postmortem: [Incident Title]
**Date:** [Date] | **Duration:** [X hours] | **Severity:** SEV[X]
**Authors:** [Names] | **Status:** Draft

### Summary
[2-3 sentence plain-language summary]

### Impact
- [Users affected]
- [Duration of impact]
- [Business impact if quantifiable]

### Timeline
| Time (UTC) | Event |
|------------|-------|
| [HH:MM] | [Event] |

### Root Cause
[Detailed explanation of what caused the incident — this is where `systematic-debugging`'s
four-phase investigation, run after mitigation, feeds in]

### 5 Whys
1. Why did [symptom]? → [Because...]
2. Why did [cause 1]? → [Because...]
3. Why did [cause 2]? → [Because...]
4. Why did [cause 3]? → [Because...]
5. Why did [cause 4]? → [Root cause]

### What Went Well
- [Things that worked]

### What Went Poorly
- [Things that didn't work]

### Action Items
| Action | Owner | Priority | Due Date |
|--------|-------|----------|----------|
| [Action] | [Person] | P0/P1/P2 | [Date] |

### Lessons Learned
[Key takeaways for the team]
```

## Tips

1. **Start writing immediately** — don't wait for complete information. Update as you learn
   more.
2. **Keep updates factual** — what we know, what we've done, what's next. No speculation.
3. **Postmortems are blameless** — focus on systems and processes, not individuals.
4. **A mitigation is not a root cause** — once the incident is resolved, run
   `systematic-debugging` properly before closing the postmortem's action items.
