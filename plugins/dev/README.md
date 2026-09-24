# dev

Développement piloté par les specs : **BMAD décide quoi faire** (jusqu'aux stories), **`story-execution` le fait** avec des sous-agents. Tous les agents et skills tournent sur **Claude Opus 5.5** (`claude-opus-5-5`) avec un niveau d'effort adapté à la tâche.

## Démarrage

1. Une fois par machine : `/plugin marketplace add jt33120/claude-toolkit` puis `/plugin install core@claude-toolkit` et `/plugin install dev@claude-toolkit`.
2. Une fois par repo : `/setup-repo` (active BMAD + security-guidance, ajoute les skills éditeurs selon la stack, initialise Graft, commite `.claude/settings.json`).
3. Au quotidien : voir `dev-playbook`.

## Skills

| Skill | Rôle | Effort |
|---|---|---|
| [dev-playbook](skills/dev-playbook/SKILL.md) | Règles du jeu : phase → outil → qui décide | low |
| [setup-repo](skills/setup-repo/SKILL.md) | Prépare un repo (manuel : `/setup-repo`) | low |
| [story-execution](skills/story-execution/SKILL.md) | Exécute une story BMAD de bout en bout via sous-agents, tient la story et sprint-status.yaml à jour | high |
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
| implementer | Implémente une tâche de story en TDD | medium |
| spec-reviewer | Vérifie que le diff respecte la story (rien de manquant, rien en trop) | high |
| code-reviewer | Revue qualité et conventions | high |
| code-simplifier | Simplifie sans changer le comportement | medium |
| silent-failure-hunter | Traque les erreurs avalées | high |
| type-design-analyzer | Qualité des types et modèles | medium |
| pr-test-analyzer | Couverture et pertinence des tests | medium |

## Installés par `setup-repo` (non copiés, suivent leur éditeur)

BMAD (`bmad-method`, `bmad-toolbox`), Anthropic `security-guidance`, skills Supabase / Neon / Vercel selon la stack, Graft.
