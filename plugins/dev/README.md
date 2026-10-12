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
| frontend-content | Choisit le contenu visible, à explorer et à détailler ; livre le produit et sa spec, sans perdre le contexte |
| frontend-direction | Suit le design system, sinon propose 3 directions ; intègre Frontend Design d'Anthropic et les catalogues UI UX Pro Max, dont le choix de graphiques |
| distill | Adaptation Impeccable : retire les redondances et le bruit, conserve les usages et reporte le contexte dans la spec |
| clarify | Adaptation Impeccable : libellés, actions, erreurs et aides courts, cohérents et compréhensibles |
| critique | Adaptation Impeccable : évalue hiérarchie, charge cognitive et clarté ; priorise les défauts avec preuves |
| layout | Adaptation Impeccable : ordre de lecture, regroupement, densité et comportement responsive |
| asset-brief | Icônes open source ou prompt Codex prêt à coller, puis intégration (favicon, icônes d'app) |
| frontend-qa | QA web/mobile en 8 niveaux, rapport de bugs normé |
| backend-standards | Couche fine au-dessus des skills officielles FastAPI, Supabase, Neon |
| tdd | Tests ciblés selon le risque, régression testée quand elle peut revenir |
| systematic-debugging | Cause racine avant correctif, voie rapide pour les bugs évidents |
| verification-before-completion | Preuve avant de dire « fini » |
| security | Plan et audit sécurité FastAPI/Supabase/Vercel/LLM |
| infra-deploy | Checklist de déploiement et incidents (Vercel, Railway, Supabase, Neon) |
| video-remotion | Montage et rendu vidéo en code avec Remotion (reels 9:16, démos, sous-titres animés) ; B-roll libre de droits Pexels/Pixabay avec suivi des crédits ; plans IA par lot via l'abonnement Grok (robot local au rythme humain) |

## Agents de revue (sur demande ou via un workflow de revue)

code-reviewer · code-simplifier · silent-failure-hunter · type-design-analyzer · pr-test-analyzer

## MCP livrés avec le plugin

Playwright MCP, Chrome DevTools MCP, shadcn MCP (`.mcp.json` Claude et `mcp.json` portable, sans clé). L'hôte doit avoir `npx` et les dépendances nécessaires ; les connexions cloud se configurent dans leur environnement.

## Installés par stack-check selon la stack

BMAD, security-guidance, skills Supabase / Neon / Vercel / FastAPI, modern-python, Graft ; frontend et mobile : voir `skills/stack-check/references/frontend-mobile.md`. Outils gratuits et open source uniquement.

## Flux frontend

`frontend-content` → design (Claude Design → `/design-sync`, ou `frontend-direction`) → build (BMAD + composants shadcn / natifs, `ui-vocabulary`) → assets (`asset-brief`) → passes ciblées (`distill`, `clarify`, `layout`, `critique`) → QA (`frontend-qa`).

Livrer **le produit et sa documentation/spec**. L'agent choisit ce qui sert l'utilisateur et garde le reste dans la spec : niveau 1, synthèse visible ; niveau 2, exploration au clic ; niveau 3, détail, calculs et preuves. Les informations nécessaires à la décision restent visibles. Choisir un chiffre, tableau, graphe ou schéma selon la question ; éviter les titres, sous-titres et paragraphes qui répètent le même message.

Les mêmes fichiers de skills sont livrés à Claude Code et Codex. Les quatre passes Impeccable sont des adaptations autonomes, sans dépendance à son CLI. Frontend Design et UI UX Pro Max complètent `frontend-direction`, sans seconde skill qui ferait doublon.

Exemples d'invocation : Claude Code `/dev:frontend-content` ou `/dev:distill` ; Codex `$frontend-content` ou `$distill` selon la découverte du plugin dans le client.
