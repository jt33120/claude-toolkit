# claude-toolkit

Marketplace personnelle de plugins Claude, utilisable dans **Claude Code** (CLI, VS Code, app) et **Cowork**. Une seule source de vérité pour toutes mes skills.

## Plugins

| Plugin | Usage | Où l'installer |
|---|---|---|
| [`core`](plugins/core) | Politique de fonctionnement transverse | Partout |
| [`dev`](plugins/dev) | Dev, design, review, sécurité, infra, data | Repos de code |
| [`business`](plugins/business) | Produit, sales, marketing, rédaction, contrats | Agents de gestion, Cowork |

## Installation

**Claude Code** (une fois par machine)

```bash
/plugin marketplace add jt33120/claude-toolkit
/plugin install core@claude-toolkit
/plugin install dev@claude-toolkit
```

Puis, dans chaque repo de code : `/setup-repo`. Il écrit et commite `.claude/settings.json` pour que toute session (locale ou cloud) retrouve le même outillage :

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

**Cowork** : ajouter la marketplace depuis l'URL du repo, puis installer `core` (et `business` quand il sera prêt).

## Outils externes (non inclus, installés par projet)

- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) : workflow agile par agents (`npx bmad-method install`)
- [Graft](https://github.com/trailhq/Graft) : graphe de connaissance du code (`npx @nanonets/graft init --agents claude --no-global`)

## Crédits

Voir [NOTICE](NOTICE).
