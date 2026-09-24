# claude-toolkit

Marketplace personnelle de plugins Claude, utilisable dans **Claude Code** (CLI, VS Code, app) et **Cowork**. Une seule source de vérité pour toutes mes skills.

## Plugins

| Plugin | Usage | Où l'installer |
|---|---|---|
| [`core`](plugins/core) | Politique de fonctionnement transverse | Partout |
| [`dev`](plugins/dev) | Dev, design, review, sécurité, infra, data | Repos de code |
| [`business`](plugins/business) | Produit, sales, marketing, rédaction, contrats | Agents de gestion, Cowork |

## Installation

**Claude Code**

```bash
/plugin marketplace add jt33120/claude-toolkit
/plugin install core@claude-toolkit
/plugin install dev@claude-toolkit        # dans un repo de code
/plugin install business@claude-toolkit   # dans un agent de gestion
```

Pour activer un plugin automatiquement dans un repo, ajouter dans `.claude/settings.json` :

```json
{
  "extraKnownMarketplaces": {
    "claude-toolkit": { "source": { "source": "github", "repo": "jt33120/claude-toolkit" } }
  },
  "enabledPlugins": { "core@claude-toolkit": true, "dev@claude-toolkit": true }
}
```

**Cowork** : ajouter la marketplace depuis l'URL du repo, puis installer les plugins voulus.

## Outils externes (non inclus, installés par projet)

- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) : workflow agile par agents (`npx bmad-method install`)
- [Graft](https://github.com/trailhq/Graft) : graphe de connaissance du code (`npx @nanonets/graft init --agents claude --no-global`)

## Crédits

Voir [NOTICE](NOTICE).
