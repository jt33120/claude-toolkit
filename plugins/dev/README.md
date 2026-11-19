# dev

Sessions de code avec BMAD (cadrage, stories, `bmad-build`, `bmad-code-review`) + qualité senior. Les interfaces sont dans [`front`](../front/README.md), la vidéo dans [`media`](../media/README.md).

## Démarrage

1. Suivre le [guide de démarrage](../../README.md) : installation dans chaque assistant, instructions persistantes par projet, puis utilisation des skills.
2. Dans Claude Code : `/dev:stack-check` déclare la stack au premier passage, puis vérifie les connexions. Utiliser `agent-bridge` pour le partage des instructions et skills avec Codex ; configurer les connecteurs dans chaque environnement.

## Skills

| Skill | Rôle |
|---|---|
| bootstrap | `/dev:bootstrap` : prépare un repo en une passe (CLAUDE.md court, plugins dans `.claude/settings.json`, stack-check, agent-bridge si Codex, audit de départ) |
| claude-md | Tient `CLAUDE.md` court et juste (80 lignes max) : ce qu'un nouvel arrivant raterait, rien d'autre ; lancé après chaque compaction |
| audit | Revue approfondie : architecture, lisibilité, erreurs silencieuses, tests, sécurité, règles du projet. `/dev:audit` (repo) ou `/dev:audit diff` (branche, avant PR) |
| stack-check | Déclare la stack et le stade du projet (poc, mvp, prod), installe les outils, vérifie lecture/écriture des MCP |
| backend-standards | Couche fine au-dessus des skills officielles FastAPI, Supabase, Neon |
| diagrams | Schémas en code versionnés : Mermaid par défaut (rendu natif GitHub), Diagram Design pour les livrables soignés (Archify si chaque élément doit être tracé au code), LikeC4 pour un modèle C4 interrogeable ; validation avant commit |
| tdd | Tests dimensionnés au stade du projet (POC : quelques tests locaux, pas de CI), puis ciblés selon le risque, tranches verticales à l'interface publique, mocks limités aux dépendances externes |
| systematic-debugging | Cause racine avant correctif : boucle de reproduction rapide, 3–5 hypothèses classées, logs de debug balisés puis retirés ; voie rapide pour les bugs évidents |
| verification-before-completion | Preuve avant de dire « fini » |
| security | Plan et audit sécurité FastAPI/Supabase/Vercel/LLM ; qualification des trouvailles (frontière, certitude, gravité) reprise de Cloudflare, sa skill complète pour les gros audits |
| wizard | Script bash interactif qui te guide dans les étapes manuelles (clés API, `.env`, secrets GitHub, migration ponctuelle) |
| infra-deploy | Checklist de déploiement et incidents (Vercel, Railway, Supabase, Neon) |

## Agents de revue (sur demande ou via un workflow de revue)

code-reviewer · code-simplifier · silent-failure-hunter · type-design-analyzer · pr-test-analyzer

## Installés par stack-check selon la stack

BMAD, security-guidance, skills Supabase / Neon / Vercel / FastAPI, modern-python, Graft ; frontend et mobile : voir `skills/stack-check/references/frontend-mobile.md` (avec le plugin `front`). Outils gratuits et open source uniquement.

## Hooks

| Moment | Effet |
|---|---|
| Après une compaction | Claude applique `claude-md` et résume en une ligne ce qui a changé |
| Ouverture d'un repo | Sans `CLAUDE.md` : propose `/dev:bootstrap`. Sans `core` activé : le signale |
| `gh pr create` / `glab mr create` | Bloqué tant que `/dev:audit diff` n'a pas validé le commit courant (marqueur hors du repo, dans `.git/`) |

Les hooks ne s'exécutent que dans un dépôt Git et ne bloquent jamais la session en cas d'erreur. Ils sont propres à Claude Code ; Codex utilise les skills sans eux.
