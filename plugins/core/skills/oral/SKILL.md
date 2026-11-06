---
name: oral
description: "Read the agent's replies aloud: `/oral on|off|status|stop|test`. Free local voice first (Piper, Windows SAPI, macOS say, Linux espeak-ng), ElevenLabs as fallback. FR : « réponds-moi à l'oral », « lis tes réponses »."
disable-model-invocation: true
argument-hint: "on | off | status | stop | test"
---

# Oral

A Stop hook shipped with the `core` plugin (`hooks/hooks.json`) speaks every final reply while the mode is **on**. The state is one flag file, `~/.claude/oral/on`, shared by every session and project; the hook returns at once when it is absent.

## Steps

1. Run the script from this skill's base directory with the user's argument (default `status`; `stop` silences the current reply): `sh "<base dir>/scripts/run.sh" <argument>`
2. Report the script's output in one line: the state, and the engine that spoke (`piper`, `voix_systeme`, `elevenlabs`). When it prints « aucun », show the last lines of `~/.claude/oral/oral.log` and the matching fix from the table below.

Done when the user has the state and the engine in one line.

While the mode is on, open each reply with one or two sentences that carry the answer and read well aloud: the listener hears the start first, and long replies are cut at `ORAL_MAX_CHARS`. Tables, code blocks and links are stripped before speaking.

## Engines and settings

Order: Piper → system voice → ElevenLabs. A later engine runs only when the earlier ones fail. Settings are environment variables, set in the `env` block of `~/.claude/settings.json` so the hook sees them; secrets stay out of the repo.

| Variable | Effect |
|---|---|
| `ORAL_ENGINE` | `local` (never ElevenLabs) or `elevenlabs` (always); default: the order above |
| `ORAL_VOICE` | System voice name (`Microsoft Hortense Desktop`, `Thomas`…); default: the first French voice |
| `ORAL_RATE` | Windows speed, -10 to 10 (default 1) |
| `ORAL_MAX_CHARS` | Characters spoken per reply (default 1500) |
| `ORAL_PIPER_MODEL` | Path of a Piper `.onnx` voice (with `piper` on the PATH): free, offline, more natural |
| `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, `ELEVENLABS_MODEL` | Fallback; default model `eleven_flash_v2_5` |

Behind a TLS-inspecting proxy, ElevenLabs uses the bundle in `SSL_CERT_FILE` or `REQUESTS_CA_BUNDLE`; verification stays on.

## Codex

Codex has no Stop hook; its `notify` program receives the finished turn. In `~/.codex/config.toml`:

```toml
notify = ["python3", "<path to this skill>/scripts/oral.py", "codex"]
```

The same flag file switches it on and off.
