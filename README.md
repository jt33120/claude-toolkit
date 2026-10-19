# claude-toolkit

Boîte à outils partagée pour **Claude Code et Codex** : des skills pour cadrer, développer, concevoir les interfaces, vérifier le résultat et gérer une activité. Chaque skill est maintenue une seule fois dans ce dépôt.

**Installer une fois dans chaque assistant → configurer chaque projet → travailler normalement à chaque session.**

## Comprendre les trois éléments

| Élément | Rôle | Quand |
|---|---|---|
| Marketplace | Le catalogue des plugins de ce dépôt | À ajouter une fois dans chaque outil |
| Plugin | Un paquet de skills et, éventuellement, de serveurs MCP | À installer et activer dans l'environnement utilisé |
| Skill | Une procédure que l'IA charge pour une tâche précise | Choisie selon la demande ou appelée explicitement |

L'IA découvre les noms et descriptions des skills, puis charge les instructions et références nécessaires à la tâche. Les règles à appliquer dans toutes les sessions d'un projet vivent dans ses fichiers d'instructions.

| Plugin | Usage | Choix de départ |
|---|---|---|
| [`core`](plugins/core/README.md) | Instructions communes, maintenance du toolkit, partage Claude/Codex | Installer pour les sessions de code |
| [`dev`](plugins/dev/README.md) | Développement, frontend, QA, sécurité, infrastructure, vidéo | Installer avec `core` pour coder |
| [`business`](plugins/business/README.md) | Produit, vente, marketing, finance, RH, contrats | Ajouter pour les usages de gestion et Cowork |

## 1. Installer une fois

### Claude Code

Dans le **terminal de l'ordinateur**, exécuter :

```bash
claude plugin marketplace add jt33120/claude-toolkit
claude plugin install core@claude-toolkit --scope user
claude plugin install dev@claude-toolkit --scope user
```

Le scope `user` rend les plugins disponibles dans les projets de cet utilisateur sur cet ordinateur. Ouvrir ensuite une nouvelle session Claude Code, ou utiliser `/reload-plugins` dans une session déjà ouverte.

Pour installer depuis une **session interactive Claude Code**, utiliser les commandes suivantes, puis choisir l'installation pour l'utilisateur :

```text
/plugin marketplace add jt33120/claude-toolkit
/plugin install core@claude-toolkit
/plugin install dev@claude-toolkit
```

**Windows avec l'extension VS Code seule** : `/plugin` n'est pas disponible dans l'extension et `claude` n'est souvent pas dans le PATH. L'extension embarque le programme en ligne de commande : l'appeler par son chemin complet, dans Git Bash ou PowerShell (adapter le numéro de version du dossier).

```bash
CLAUDE=~/.vscode/extensions/anthropic.claude-code-*-win32-x64/resources/native-binary/claude.exe
$CLAUDE plugin marketplace add jt33120/claude-toolkit
$CLAUDE plugin install core@claude-toolkit --scope user
$CLAUDE plugin install dev@claude-toolkit --scope user
```

Puis recharger la fenêtre VS Code. Vérifier avec `claude plugin list` dans le terminal, ou `/plugin` dans la session. Taper `/` doit faire apparaître les skills avec leur préfixe, par exemple `/dev:frontend-content`.

### Codex local et application de bureau

Dans le **terminal**, ajouter le catalogue :

```bash
codex plugin marketplace add jt33120/claude-toolkit
```

Dans le catalogue **Plugins de l'application de bureau**, sélectionner la source `claude-toolkit`, puis installer et activer `core` et `dev`. Ouvrir une nouvelle discussion. Dans Codex CLI ou l'extension IDE, `/skills` ou `$` permet de retrouver les skills disponibles.

Si le client utilisé ne propose pas cette installation, suivre le [guide agent-bridge](plugins/core/skills/agent-bridge/SKILL.md) : un clone local du toolkit peut exposer les mêmes skills à Codex, avec des liens ou des copies gérées.

### Cowork et sessions cloud

Dans Cowork, ajouter la marketplace depuis l'URL de ce dépôt, puis installer `core` et `business` selon le besoin.

L'installation locale reste propre à l'environnement utilisé. Une session cloud a sa propre configuration ; les plugins installés sur l'ordinateur ne s'y transfèrent pas automatiquement. Pour Claude Code dans le navigateur, ne pas compter sur les seuls plugins locaux ou sur `.claude/settings.json` pour les charger.

**Claude Code sur le web (sessions cloud)** : coller ce script dans le **Setup script** de l'environnement (menu de l'environnement cloud dans la barre de titre d'une session → Edit). Il s'exécute au démarrage de chaque nouvelle session, avant Claude Code, pour tous les dépôts de cet environnement ; il peut être relancé sans erreur.

```bash
claude plugin marketplace add jt33120/claude-toolkit >/dev/null 2>&1 || claude plugin marketplace update claude-toolkit
for p in core dev business; do
  claude plugin install "$p@claude-toolkit" --scope user || true
  claude plugin update "$p@claude-toolkit" || true
done
```

Retirer `business` de la boucle si l'environnement ne sert qu'au code. Vérifier dans une nouvelle session : `/` doit lister `/dev:…` et `/core:…`.

Le plugin `dev` fournit Playwright MCP, Chrome DevTools MCP et shadcn MCP. Leur exécution locale demande `npx`, les dépendances nécessaires et l'accès réseau. Si un serveur Playwright MCP est déjà configuré sur le poste (navigateur précis, profil), les deux coexistent ; désactiver celui du plugin avec `/mcp` s'il ouvre le mauvais navigateur. Derrière un proxy d'entreprise qui bloque `npx`, ces serveurs ne démarrent pas, sans effet sur les skills. Configurer les comptes et autorisations des autres connecteurs dans chaque environnement.

### Recevoir les mises à jour automatiquement

Rien à réinstaller : chaque nouvelle version publiée (numéro de version du plugin augmenté) arrive par mise à jour. Pour une marketplace tierce comme celle-ci, la mise à jour automatique est désactivée par défaut ; l'activer une fois par poste dans les réglages utilisateur (`~/.claude/settings.json`, sous Windows `%USERPROFILE%\.claude\settings.json`) en ajoutant `autoUpdate` à l'entrée existante :

```json
{
  "extraKnownMarketplaces": {
    "claude-toolkit": {
      "source": { "source": "github", "repo": "jt33120/claude-toolkit" },
      "autoUpdate": true
    }
  }
}
```

Claude Code rafraîchit alors la marketplace et met à jour les plugins en arrière-plan après le démarrage ; la nouvelle version est chargée à la session suivante (ou après `/reload-plugins`). Équivalent dans le terminal : `/plugin` → Marketplaces → claude-toolkit → Enable auto-update. Mise à jour manuelle immédiate : `claude plugin marketplace update claude-toolkit` puis `claude plugin update dev@claude-toolkit`.

Les sessions cloud se mettent à jour par le script de setup ci-dessus, à chaque démarrage. Codex et Cowork ont leur propre gestion des mises à jour dans leur catalogue de plugins.

## 2. Configurer chaque projet une fois

Dans le projet, demander à l'IA :

> Utilise agent-bridge pour configurer les instructions communes à Claude Code et Codex. Conserve les fichiers existants. Inscris dans AGENTS.md l'obligation d'utiliser frontend-content avant de construire ou modifier un front, de livrer le produit et sa spec, puis de vérifier le résultat avec les skills frontend adaptées. Vérifie que les skills demandées sont disponibles dans cet environnement.

Les règles communes vont dans **`AGENTS.md`**, à la racine du projet. Pour les partager avec Claude Code, ajouter cette ligne dans **`CLAUDE.md`**, en conservant ses autres instructions :

```markdown
@AGENTS.md
```

Le [guide agent-bridge](plugins/core/skills/agent-bridge/SKILL.md) détaille la migration, les liens/copies de skills et la configuration MCP. Garder les consignes propres à Claude dans `CLAUDE.md`. Versionner les instructions communes avec le projet pour les retrouver dans les prochaines sessions.

Pour les interfaces, ajouter à `AGENTS.md` :

```markdown
- Avant de construire ou modifier un écran, utiliser frontend-content.
- Livrer le produit et sa spec ; choisir synthèse, exploration et détail.
- Conserver le contexte dans la spec et supprimer le texte UI redondant.
- Choisir un chiffre, un tableau, un graphe ou un schéma selon la question.
- Garder l'information décisive visible au moment de l'action.
- Vérifier le résultat avec les passes frontend utiles puis frontend-qa.
```

Pour déclarer les outils du projet dans Claude Code, lancer **`/dev:stack-check`**. Au premier passage, cette skill recueille la stack et prépare les fichiers de configuration et outils adaptés. Elle présente les changements et demande l'accord avant le commit. Aux passages suivants, elle vérifie les connexions existantes.

`stack-check` prépare principalement la configuration Claude. Utiliser `agent-bridge` pour le partage avec Codex et configurer ses connecteurs dans l'environnement où il s'exécute.

## 3. Utiliser les skills à chaque session

Après la configuration, donner la tâche normalement : « construis cet écran », « simplifie cette interface », « corrige ce bug ». Les skills peuvent être sélectionnées automatiquement quand leur description correspond à la demande.

Pour demander explicitement une passe :

| Besoin | Claude Code | Codex CLI / IDE |
|---|---|---|
| Partager les instructions Claude/Codex | `/core:agent-bridge` | `$agent-bridge` |
| Vérifier la stack | `/dev:stack-check` | `$stack-check` |
| Concevoir le contenu du front et sa spec | `/dev:frontend-content` | `$frontend-content` |
| Choisir une direction visuelle | `/dev:frontend-direction` | `$frontend-direction` |
| Alléger un écran | `/dev:distill` | `$distill` |
| Clarifier les libellés et messages | `/dev:clarify` | `$clarify` |
| Évaluer le design | `/dev:critique` | `$critique` |
| Revoir la mise en page | `/dev:layout` | `$layout` |
| Vérifier le frontend | `/dev:frontend-qa` | `$frontend-qa` |
| Chercher la cause d'un bug | `/dev:systematic-debugging` | `$systematic-debugging` |
| Faire ou mettre à jour un schéma | `/dev:diagrams` | `$diagrams` |
| Mettre un plan à l'épreuve | `/core:grilling` | `$grilling` |
| Guider une configuration manuelle (clés, secrets) | `/dev:wizard` | `$wizard` |

Dans Codex, choisir la skill dans `/skills` ou le sélecteur `$` si son nom est présenté avec un namespace. Une skill absente du sélecteur doit d'abord être installée ou activée dans cet environnement.

Exemple dans Claude Code :

```text
/dev:frontend-content Construis l'écran de comparaison des offres.
Conserve les hypothèses dans la spec et rends les calculs accessibles au clic.
```

Exemple dans Codex :

```text
$distill Simplifie cet écran en conservant les fonctionnalités
et le contexte dans sa spec.
```

Lors d'un changement d'agent en cours de travail, `agent-bridge` prévoit une courte passation dans `.agents/HANDOFF.md` : objectif, travail terminé, prochaine étape et questions ouvertes.

## Parcours frontend : produit et spec

`frontend-content` → `frontend-direction` → réalisation → passes ciblées (`distill`, `clarify`, `layout`, `critique`) → `frontend-qa`.

Livrer **le produit utilisable et sa documentation/spec**. Trois niveaux : **synthèse visible → exploration au clic → détail**. Les prix, erreurs, conséquences et hypothèses qui changent la décision restent visibles au bon moment. Chaque visuel répond à une question.

Les passes `distill`, `clarify`, `critique` et `layout` sont adaptées d'Impeccable. Frontend Design d'Anthropic et les références UI UX Pro Max, dont le choix des graphiques, sont intégrés à `frontend-direction`.

Voir le [modèle de spec](plugins/dev/skills/frontend-content/references/content-spec-template.md), les [exemples de répartition du contenu](plugins/dev/skills/frontend-content/references/examples.md) et le [flux frontend détaillé](plugins/dev/README.md#flux-frontend).

## Mettre à jour

Dans le **terminal**, pour Claude Code :

```bash
claude plugin marketplace update claude-toolkit
claude plugin update core@claude-toolkit
claude plugin update dev@claude-toolkit
```

Mettre également à jour `business@claude-toolkit` s'il est installé. Dans une session, `/plugin marketplace update claude-toolkit` rafraîchit le catalogue ; l'onglet Installed de `/plugin` permet de mettre à jour chaque plugin avec **Update now**. Ouvrir une nouvelle session ou suivre l'indication de rechargement.

Pour Codex, rafraîchir la marketplace :

```bash
codex plugin marketplace upgrade claude-toolkit
```

Puis vérifier et mettre à jour les plugins installés dans le catalogue de l'application. Pour un clone utilisé via `agent-bridge`, mettre à jour le clone et relancer le bridge si des copies gérées doivent être rafraîchies. Dans Cowork, mettre à jour le plugin depuis la marketplace.

## Configuration avancée

<details>
<summary>Activer le toolkit et BMAD dans un projet Claude Code</summary>

La configuration de projet complète l'installation dans cet environnement. Chaque poste doit disposer des plugins activés ; une session cloud utilise ses propres possibilités de chargement.

Exemple à **fusionner** dans `.claude/settings.json` en conservant les réglages existants. Activer les entrées BMAD et security-guidance uniquement si ces outils sont utilisés et installés :

```json
{
  "extraKnownMarketplaces": {
    "claude-toolkit": { "source": { "source": "github", "repo": "jt33120/claude-toolkit" } },
    "bmad": { "source": { "source": "github", "repo": "bmad-code-org/bmad-plugins" } },
    "claude-code-plugins": { "source": { "source": "github", "repo": "anthropics/claude-code" } }
  },
  "enabledPlugins": {
    "core@claude-toolkit": true,
    "dev@claude-toolkit": true,
    "bmad-method@bmad": true,
    "bmad-toolbox@bmad": true,
    "security-guidance@claude-code-plugins": true
  }
}
```

Le plugin BMAD donne accès à ses agents et skills. Le projet doit aussi être initialisé : suivre la skill BMAD de setup ; `stack-check` vérifie d'abord si cette initialisation existe déjà.

</details>

Les catalogues de ce dépôt sont `.claude-plugin/marketplace.json` pour Claude et `.agents/plugins/marketplace.json` pour les hôtes compatibles. Les manifests portables `plugins/*/plugin.json` et le `mcp.json` de `dev` complètent les fichiers Claude.

Pour importer une configuration Claude dans Codex local, voir `agent-bridge` et la commande `/import` lorsque le client la propose. L'import reprend la configuration choisie ; appeler Claude Code depuis Codex reste une opération distincte.

## Vérifier le toolkit

Depuis un clone du dépôt :

```bash
python3 scripts/validate_toolkit.py
python3 -m unittest discover -s tests
```

Le contrôle valide les manifests, noms et descriptions de skills, chemins de référence et CSV de styles. Il s'exécute aussi sur les PR via GitHub Actions. La table `styles.csv` contient les identifiants 1–58 et 71–89 ; les identifiants 59–70 sont absents de la source et ne sont pas inventés.

## Outils externes

Ces outils se configurent par projet selon le besoin :

- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) : cadrage et réalisation par agents ; suivre son workflow de setup.
- [Graft](https://github.com/trailhq/Graft) : graphe de connaissance du code, initialisé par `stack-check` lorsqu'il fait partie du setup.
- [public-apis](https://github.com/public-apis/public-apis) : catalogue à consulter avant d'ajouter une dépendance ou un service externe.

## Documentation officielle et crédits

- [Claude Code : installer et gérer les plugins](https://code.claude.com/docs/en/discover-plugins)
- [Claude Code : utiliser les skills](https://code.claude.com/docs/en/skills)
- [Claude Code : partager les instructions de projet](https://code.claude.com/docs/en/memory)
- [OpenAI : plugins et marketplaces](https://developers.openai.com/plugins/build/plugins)
- [OpenAI : utiliser et distribuer les skills](https://learn.chatgpt.com/docs/build-skills)

Sources et licences des adaptations : [NOTICE](NOTICE).
