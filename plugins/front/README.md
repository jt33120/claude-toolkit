# front

Interfaces web et mobile : contenu et spec, direction visuelle, passes ciblées et QA. À activer avec `core` et `dev` dans les projets qui ont une interface.

## Skills

| Skill | Rôle |
|---|---|
| frontend-content | Choisit le contenu visible, à explorer et à détailler ; livre le produit et sa spec, sans perdre le contexte |
| frontend-direction | Suit le design system, sinon propose 3 directions ; intègre Frontend Design d'Anthropic et les catalogues UI UX Pro Max, dont le choix de graphiques ; socle anti-rendu générique (Hallmark, Taste Skill) |
| distill | Adaptation Impeccable : retire les redondances et le bruit, conserve les usages et reporte le contexte dans la spec |
| clarify | Adaptation Impeccable : libellés, actions, erreurs et aides courts, cohérents et compréhensibles |
| critique | Adaptation Impeccable : évalue hiérarchie, charge cognitive et clarté ; priorise les défauts avec preuves |
| layout | Adaptation Impeccable : ordre de lecture, regroupement, densité et comportement responsive |
| ui-vocabulary | Nom exact, variantes, équivalents web/iOS/Android et alternatives de 152 composants et patterns |
| asset-brief | Icônes open source ou prompt Codex prêt à coller, puis intégration (favicon, icônes d'app) |
| frontend-qa | QA web/mobile en 8 niveaux, rapport de bugs normé |

## MCP livrés avec le plugin

Playwright MCP, Chrome DevTools MCP, shadcn MCP (`.mcp.json` Claude et `mcp.json` portable, sans clé, versions fixées : les monter volontairement dans les deux fichiers). L'hôte doit avoir `npx` et les dépendances nécessaires ; les connexions cloud se configurent dans leur environnement.

## Flux frontend

`frontend-content` → design (Claude Design → `/design-sync`, ou `frontend-direction`) → build (BMAD + composants shadcn / natifs, `ui-vocabulary`) → assets (`asset-brief`) → passes ciblées (`distill`, `clarify`, `layout`, `critique`) → QA (`frontend-qa`).

Livrer **le produit et sa documentation/spec**. L'agent choisit ce qui sert l'utilisateur et garde le reste dans la spec : niveau 1, synthèse visible ; niveau 2, exploration au clic ; niveau 3, détail, calculs et preuves. Les informations nécessaires à la décision restent visibles. Choisir un chiffre, tableau, graphe ou schéma selon la question ; éviter les titres, sous-titres et paragraphes qui répètent le même message.

Les mêmes fichiers de skills sont livrés à Claude Code et Codex. Les quatre passes Impeccable sont des adaptations autonomes, sans dépendance à son CLI. Frontend Design et UI UX Pro Max complètent `frontend-direction`, sans seconde skill qui ferait doublon.

Exemples d'invocation : Claude Code `/front:frontend-content` ou `/front:distill` ; Codex `$frontend-content` ou `$distill` selon la découverte du plugin dans le client.
