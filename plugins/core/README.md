# core

Installé partout (Claude Code niveau utilisateur, Cowork, agents).

| Skill | Rôle |
|---|---|
| [toolkit-maintainer](skills/toolkit-maintainer/SKILL.md) | Toute création ou modification de skill passe par ce repo |
| [writing-voice](skills/writing-voice/SKILL.md) | Textes dans la voix du projet, sans tics d'IA : profil de voix interactif (`.claude/voice.md`), format selon le support, contrôle par script (`ai_tells.py`, FR et EN), apprentissage à partir de tes corrections |
| [language-strategy](skills/language-strategy/SKILL.md) | Anglais pour travailler (prompts, specs, code, briefs d'agents), langue du public pour livrer ; glossaire par projet, réécriture native plutôt que traduction |
| [ci-budget](skills/ci-budget/SKILL.md) | Réduit les minutes GitHub Actions sans supprimer de vrais tests : mesure par workflow, CI alignée sur le rythme BMAD, déclencheurs, concurrence, cache |
| [agent-bridge](skills/agent-bridge/SKILL.md) | Pont Claude Code ↔ Codex : migration prudente de `AGENTS.md` / `CLAUDE.md`, copies suivies sous Windows, skills, MCP et passation |

Complément recommandé dans Claude Code (passe finale pour l'anglais) : `npx skills add blader/humanizer -a claude-code -y`.
