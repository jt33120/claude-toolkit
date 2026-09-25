---
name: toolkit-maintainer
description: 'Use whenever the user asks to create, write, modify, improve, rename, merge, move or delete a toolkit skill for Claude Code or Codex, or to add one to a plugin (FR : « crée une skill », « modifie la skill », « ajoute au plugin », « fusionne ces skills », « supprime la skill »). Maintain the shared source in the claude-toolkit repo (github.com/jt33120/claude-toolkit).'
---

# Toolkit maintainer

Source unique de vérité des skills : **github.com/jt33120/claude-toolkit**. Chaque skill vit dans un seul plugin :

| Plugin | Contexte d'usage |
|---|---|
| `core` | Transverse, installé partout |
| `dev` | Sessions de code : dev, design, review, sécurité, infra, data |
| `business` | Agents de gestion : produit, sales, marketing, rédaction, audit, contrats |

## Règles

1. **Jamais de skill isolée** (upload sur le compte, `~/.claude/skills`, `.claude/skills` d'un repo, mini-plugin). Exception : une skill perso que l'utilisateur demande explicitement de garder hors repo.
2. **Pas de doublon.** Avant de créer, lister les descriptions existantes (`plugins/*/skills/*/SKILL.md`). Si une skill couvre déjà plus de la moitié du besoin, l'étendre plutôt qu'en créer une nouvelle.
3. **Choisir le plugin selon le contexte d'usage**, pas selon le sujet.
4. **Structure** : `plugins/<plugin>/skills/<nom-kebab>/SKILL.md`, plus `references/`, `scripts/`, `assets/` si utile. Le `name` du frontmatter = nom du dossier. La `description` dit *quand* l'utiliser, avec déclencheurs FR et EN, moins de 1024 caractères, et ne recoupe aucune autre description.
5. **Repo public** : aucun nom de client ou de personne, e-mail, chemin personnel, token ou secret. Anonymiser (« le client », « l'utilisateur »).
6. **Contenu tiers** : en-tête de provenance et licence dans la skill, et mise à jour de `NOTICE`.
7. **Versionner ensemble** `plugins/<plugin>/.claude-plugin/plugin.json` et `plugins/<plugin>/plugin.json` : patch = correction, minor = nouvelle skill ou changement de comportement, major = suppression ou renommage. Mettre à jour `mcp.json` portable si `.mcp.json` change.
8. **Mettre à jour** le tableau du `README.md` du plugin (skill | rôle | statut).

## Workflow

1. Reformuler le besoin et proposer : nom, plugin, création ou extension d'une skill existante.
2. Pour une création, une suppression ou un renommage : faire valider par l'utilisateur avant d'écrire.
3. Rédiger la skill (courte, instructions actionnables, pas de théorie).
4. Lancer `python3 scripts/validate_toolkit.py` et les tests pertinents. Pousser en **un seul commit** via l'outil GitHub MCP (skill + README du plugin + les deux manifests + NOTICE si besoin). Message : `<plugin>: <verbe> <skill> — <pourquoi>`.
   Sans MCP GitHub : `git` si des identifiants sont disponibles, sinon livrer les fichiers et le chemin exact où les placer.
5. Terminer par :
   - la commande de mise à jour : Claude Code `/plugin marketplace update claude-toolkit` ; Cowork : mettre à jour le plugin depuis la marketplace ;
   - s'il existe une ancienne version de la skill ailleurs (compte, dossier local, autre plugin), dire laquelle supprimer et où.
