# Pre-Deploy Checklist

Generate and work through a pre-deployment checklist to verify readiness before shipping,
for a Vercel (frontend) + Railway (backend/workers) + Supabase/Neon (Postgres) + GitHub
Actions stack.

## Output

```markdown
## Deploy Checklist: [Service/Release]
**Date:** [Date] | **Deployer:** [Name]

### Pre-Deploy
- [ ] All GitHub Actions checks passing on the release branch/PR
- [ ] Code reviewed and approved
- [ ] No known critical bugs in release
- [ ] Database migrations tested against a Neon branch or Supabase preview branch
- [ ] Feature flags configured (if applicable)
- [ ] Environment variables present in Vercel (prod + preview) and Railway for anything new
- [ ] Rollback plan documented
- [ ] On-call / whoever's watching notified

### Deploy
- [ ] Deploy to a Vercel preview / Railway staging environment and verify
- [ ] Run smoke tests (see `frontend-qa` for a browser-level check)
- [ ] Deploy to production (Vercel promotes the build; Railway redeploys the service)
- [ ] Monitor error rates and latency for 15 min (Vercel/Railway logs and metrics, or
      Sentry/monitoring if connected)
- [ ] Verify key user flows

### Post-Deploy
- [ ] Confirm metrics are nominal
- [ ] Update release notes / changelog
- [ ] Notify stakeholders
- [ ] Close related tickets/issues

### Rollback Triggers
- Error rate exceeds [X]%
- P50/P95 latency exceeds [X]ms
- [Critical user flow] fails
```

## Step-by-Step

### 1. CI status

Pull the release diff and check GitHub Actions status before anything else:
- Use the GitHub MCP connector (or `gh pr checks`, `gh run list`) to confirm every required
  check on the branch/PR is green.
- Confirm the PR is reviewed and approved — don't deploy an unreviewed diff.

### 2. Database migrations

If the release includes a schema change:
- **Supabase**: check `supabase migration list` (or the Supabase MCP connector) for pending
  migrations; apply and test against a Supabase preview branch first, never directly against
  production.
- **Neon**: if the workflow uses Neon branching, create a throwaway branch from production
  (Neon MCP connector or `neonctl branches create`), run the migration there, verify the app
  against it, then apply to the real target.
- Confirm the migration is backward-compatible with the currently-deployed code for the
  window between "migration applied" and "new code deployed" — a migration that drops a
  column the old code still reads will break the old deployment during rollout.

### 3. Environment variables

- **Vercel**: confirm any new env vars exist for both `production` and `preview` environments
  (Vercel MCP connector, or `vercel env ls`). A var only set in `preview` silently breaks prod.
- **Railway**: confirm the service's variables include anything new (Railway MCP connector,
  or `railway variables`).
- Never put a service-role/secret key in a `NEXT_PUBLIC_*` var or anything shipped to the
  browser — see the `security` skill for the Supabase `service_role` vs `anon` key distinction.

### 4. Feature flags

If flags gate the change, confirm the flag exists, is off by default in production, and there
is a documented plan for the rollout percentage/schedule.

### 5. Rollback plan

Decide and write down, before deploying, not during an incident:
- **Vercel**: rollback is "promote the previous deployment" — confirm you know which one.
- **Railway**: rollback is "redeploy the previous image/build" — confirm the previous
  deployment is still available (Railway keeps deploy history).
- If a migration was applied, is it reversible? If not, the rollback plan is "roll forward
  with a fix," not "roll back" — say so explicitly.

### 6. Deploy and verify

- Deploy to preview/staging first (Vercel preview deployment, Railway staging environment)
  and verify there before touching production.
- Run smoke tests — for anything user-facing, the `frontend-qa` skill covers driving a
  real browser against the preview URL.
- Promote to production. Watch error rates and latency for at least 15 minutes using
  whichever of Vercel/Railway logs, metrics, or a connected monitoring tool (e.g. Sentry) is
  available.
- Verify the key user flows the release touches, by hand or via `frontend-qa`.

### 7. Post-deploy

- Confirm metrics are nominal against the rollback triggers you wrote down in step 5.
- Update the changelog/release notes.
- Notify whoever needs to know; close the related issue/ticket.

## Customization

Tell me about your deploy and this checklist adapts:
- "We use feature flags" → adds flag verification steps
- "This includes a database migration" → expands the Supabase/Neon migration section
- "This is a breaking API change" → adds consumer notification steps
- "No Railway service involved" → drops the Railway-specific steps

## Tips

1. **Run before every deploy** — even routine ones. Checklists prevent "I forgot to..."
2. **Customize once, reuse** — tell this skill your stack details once and it remembers them
   for the session.
3. **Decide rollback criteria before deploying, not during** — an incident is the wrong time
   to be inventing your error-rate threshold.