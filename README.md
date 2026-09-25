# claude-toolkit

Marketplace de plugins pour **Claude Code**, **Codex** et les surfaces qui acceptent les plugins portables. Chaque skill est maintenue une seule fois dans ce dépôt ; l'installation et les connecteurs restent propres à chaque environnement.

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

Puis, dans chaque repo de code : `/stack-check`. Il déclare la stack exacte du projet, écrit et commite `.claude/settings.json` pour que toute session (locale ou cloud) retrouve le même outillage, et vérifie ensuite à chaque session que chaque brique reste connectée en lecture/écriture :

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

**Cowork** : ajouter la marketplace depuis l'URL du repo, puis installer `core` et, selon les besoins, `business`.

**Codex local / app de bureau** : ajouter le catalogue de ce dépôt avec `codex plugin marketplace add jt33120/claude-toolkit`, puis choisir `core`, `dev` et/ou `business` dans le catalogue. Un clone local expose également `.agents/plugins/marketplace.json` ; l'installation et l'activation s'effectuent dans le client. Les manifests portables `plugins/*/plugin.json` et le `mcp.json` de `dev` complètent les manifests Claude ; les serveurs MCP locaux exigent `npx`, leurs paquets et les permissions réseau adaptées. L'installation des fichiers sur une machine ne rend pas automatiquement le plugin disponible dans une conversation Work ou un agent cloud : l'y installer/configurer séparément.

**Projet commun Claude + Codex** : utiliser la skill `agent-bridge` pour maintenir `AGENTS.md`, son import `@AGENTS.md` dans `CLAUDE.md`, les skills de projet et une passation. Son script protège les fichiers existants ; les liens locaux et les copies Windows doivent être synchronisés sur chaque poste. Dans une session Codex locale au terminal, `/import` reprend les éléments Claude Code choisis sans lancer Claude ; appeler réellement Claude Code reste un workflow local distinct.

## Vérifier le toolkit

```bash
python3 scripts/validate_toolkit.py
python3 -m unittest discover -s tests
```

Le contrôle léger valide manifests, noms et descriptions de skills, chemins de référence et CSV de styles. Il s'exécute aussi sur les PR via GitHub Actions. La table `styles.csv` contient actuellement les identifiants 1–58 et 71–89 ; les identifiants 59–70 sont absents de la source et ne sont pas inventés.

## Outils externes (non inclus, installés par projet)

- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) : workflow agile par agents (`npx bmad-method install`)
- [Graft](https://github.com/trailhq/Graft) : graphe de connaissance du code (`npx @nanonets/graft init --agents claude --no-global`)

## Crédits

Voir [NOTICE](NOTICE).
