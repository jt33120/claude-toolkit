# dev

Développement piloté par les specs : **BMAD décide quoi faire** (jusqu'aux stories) **et le construit** (`bmad-build`, `bmad-code-review`) ; ce plugin ajoute la vérification de stack, les standards, et la revue/sécurité/déploiement autour. Tous les agents et skills tournent sur **Claude Opus 5.5** (`claude-opus-5-5`) avec un niveau d'effort adapté à la tâche.

## Démarrage

1. **Une fois par machine** : `/plugin marketplace add jt33120/claude-toolkit` puis `/plugin install core@claude-toolkit` et `/plugin install dev@claude-toolkit`.
2. **Une fois par projet** : `/stack-check` — déclare la stack exacte (DB, backend, front, repo), câble `.claude/settings.json` (BMAD, security-guidance, skills éditeurs), initialise Graft et BMAD, ajoute les règles de workflow à `CLAUDE.md`.
3. **Au quotidien** : `/stack-check` en début de session pour confirmer que chaque brique est bien connectée en lecture/écriture ; BMAD pour cadrer (PRD → architecture → stories) ; Claude Design pour l'UI ; revue (`bmad-code-review`, `/code-review`, `/security-review`) avant merge.

## Skills

| Skill | Rôle | Effort |
|---|---|---|
| [stack-check](skills/stack-check/SKILL.md) | Déclare/vérifie la stack connectée en MCP (lecture + écriture) ; initialise le repo au premier lancement | low |
| [backend-standards](skills/backend-standards/SKILL.md) | Standards senior FastAPI, Node/TS, Postgres, design d'API | medium |
| [tdd](skills/tdd/SKILL.md) | Test-driven development strict | medium |
| [systematic-debugging](skills/systematic-debugging/SKILL.md) | Cause racine avant correctif | high |
| [verification-before-completion](skills/verification-before-completion/SKILL.md) | Preuve (tests, lint, types) avant de dire « fini » | low |
| [webapp-testing](skills/webapp-testing/SKILL.md) | Tests E2E Playwright | medium |
| [security](skills/security/SKILL.md) | Sécurité stack FastAPI/Supabase/Vercel/LLM + script d'audit | high |
| [infra-deploy](skills/infra-deploy/SKILL.md) | Checklist de déploiement et réponse à incident (Vercel, Railway, Supabase, Neon) | medium |

## Agents (tous `model: claude-opus-5-5`)

| Agent | Rôle | Effort |
|---|---|---|
| code-reviewer | Revue qualité et conventions | high |
| code-simplifier | Simplifie sans changer le comportement | medium |
| silent-failure-hunter | Traque les erreurs avalées | high |
| type-design-analyzer | Qualité des types et modèles | medium |
| pr-test-analyzer | Couverture et pertinence des tests | medium |

Ces agents ne se déclenchent que sur demande explicite ou en `subagent_type` explicite — pas automatiquement à chaque diff.

## Installés par `stack-check` (non copiés, suivent leur éditeur)

- **BMAD** (`bmad-method`, `bmad-toolbox`) — cadrage et exécution des stories (`bmad-build`, `bmad-code-review`)
- **Anthropic `security-guidance`** — rappel de sécurité intégré
- **Skills éditeurs selon la stack déclarée** : Supabase (`supabase`, `supabase-postgres-best-practices`), Neon (`neon-postgres`), Vercel/React (`react-best-practices`, `web-design-guidelines`, `vercel-optimize`), FastAPI (`fastapi`), Python (`modern-python` de Trail of Bits)
- **Graft** — graphe de code pour la navigation

## Workflow, en 3 étapes

1. **Installer les plugins** — une fois par machine (`core` + `dev`).
2. **`/stack-check`** — une fois par projet, pour initialiser (settings, skills, Graft, BMAD, `CLAUDE.md`).
3. **Chaque session** — `/stack-check` pour confirmer les connexions, puis BMAD pour cadrer/construire, Claude Design pour l'UI, revue avant merge.
