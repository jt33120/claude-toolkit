# core

Installé partout (Claude Code niveau utilisateur, Cowork, agents).

| Skill | Rôle | Effort |
|---|---|---|
| [toolkit-maintainer](skills/toolkit-maintainer/SKILL.md) | Toute création ou modification de skill passe par ce repo | low |
| [writing-voice](skills/writing-voice/SKILL.md) | Textes dans la voix du projet, sans tics d'IA : profil de voix interactif (`.claude/voice.md`), format selon le support, contrôle par script (`ai_tells.py`, FR et EN), apprentissage à partir de tes corrections | medium |
| [language-strategy](skills/language-strategy/SKILL.md) | Anglais pour travailler (prompts, specs, code, briefs d'agents), langue du public pour livrer ; glossaire par projet, réécriture native plutôt que traduction | low |

Complément recommandé dans Claude Code (passe finale pour l'anglais) : `npx skills add blader/humanizer -a claude-code -y`.
