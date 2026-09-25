# dev

Développement avec BMAD (cadrage, stories, `bmad-build`, `bmad-code-review`) + qualité senior.

## Démarrage

1. Une fois par machine : `/plugin marketplace add jt33120/claude-toolkit`, `/plugin install core@claude-toolkit`, `/plugin install dev@claude-toolkit`.
2. Par projet : `/stack-check` — déclare la stack, branche tout (première fois), puis vérifie à chaque session que chaque outil est connecté en lecture et écriture.

## Skills

| Skill | Rôle |
|---|---|
| stack-check | Déclare la stack, installe les outils, vérifie lecture/écriture des MCP |
| ui-vocabulary | Nom exact, variantes, équivalents web/iOS/Android et alternatives de 152 composants et patterns |
| frontend-direction | Suit le design system, sinon propose 3 directions contrastées et enregistre le choix |
| asset-brief | Icônes open source ou prompt Codex prêt à coller, puis intégration (favicon, icônes d'app) |
| frontend-qa | QA web/mobile en 8 niveaux, rapport de bugs normé |
| backend-standards | Couche fine au-dessus des skills officielles FastAPI, Supabase, Neon |
| tdd | Tests ciblés selon le risque, régression testée quand elle peut revenir |
| systematic-debugging | Cause racine avant correctif, voie rapide pour les bugs évidents |
| verification-before-completion | Preuve avant de dire « fini » |
| security | Plan et audit sécurité FastAPI/Supabase/Vercel/LLM |
| infra-deploy | Checklist de déploiement et incidents (Vercel, Railway, Supabase, Neon) |

## Agents de revue (sur demande ou via un workflow de revue)

code-reviewer · code-simplifier · silent-failure-hunter · type-design-analyzer · pr-test-analyzer

## MCP livrés avec le plugin

Playwright MCP, Chrome DevTools MCP, shadcn MCP (`.mcp.json` Claude et `mcp.json` portable, sans clé). L'hôte doit avoir `npx` et les dépendances nécessaires ; les connexions cloud se configurent dans leur environnement.

## Installés par stack-check selon la stack

BMAD, security-guidance, skills Supabase / Neon / Vercel / FastAPI, modern-python, Graft ; frontend et mobile : voir `skills/stack-check/references/frontend-mobile.md`. Outils gratuits et open source uniquement.

## Flux frontend

Design (Claude Design → `/design-sync`, ou `frontend-direction`) → build (BMAD + composants shadcn / natifs, `ui-vocabulary`) → assets (`asset-brief`, handoff Codex) → QA (`frontend-qa`) → audit (impeccable, web-design-guidelines).
