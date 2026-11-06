#!/usr/bin/env python3
"""Read the agent's replies aloud.

    oral.py on | off | status | stop     toggle (state: ~/.claude/oral/on)
    oral.py test | say "text"            speak a sample or a text now
    oral.py hook                         Claude Code Stop hook: JSON on stdin
    oral.py codex '<json>'               Codex `notify` program: JSON as last argument

Engines, in order: a free local voice (Piper if configured, otherwise the OS voice:
Windows SAPI, macOS `say`, Linux spd-say/espeak-ng), then ElevenLabs when the local
voice fails and ELEVENLABS_API_KEY is set. ORAL_ENGINE=local|elevenlabs forces one.
Standard library only; speech runs detached so the agent never waits for it.
"""
import json
import os
import re
import shutil
import signal
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ETAT = Path.home() / ".claude" / "oral"
DRAPEAU = ETAT / "on"
PID = ETAT / "pid"
JOURNAL = ETAT / "oral.log"
MAX = int(os.environ.get("ORAL_MAX_CHARS", "1500"))
WINDOWS = sys.platform == "win32"
MAC = sys.platform == "darwin"


def log(msg):
    ETAT.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")


# ---------------------------------------------------------------- text
def nettoyer(md: str) -> str:
    """Markdown -> plain sentences worth hearing."""
    t = re.sub(r"```.*?```", " ", md, flags=re.S)                    # code blocks
    t = re.sub(r"`?✶ Insight[^\n]*\n.*?\n`?─{5,}`?", " ", t, flags=re.S)  # insight boxes
    lignes = []
    for l in t.splitlines():
        s = l.strip()
        if re.fullmatch(r"[|:\-\s─`]+", s or "-"):                   # rules, table separators
            continue
        if s.startswith("|"):                                         # table row -> list
            s = ", ".join(c.strip() for c in s.strip("|").split("|") if c.strip())
        s = re.sub(r"^#{1,6}\s*", "", s)                              # headings
        s = re.sub(r"^([-*+]|\d+[.)])\s+", "", s)                     # bullets
        s = re.sub(r"^>\s?", "", s)                                   # quotes
        if s and not re.search(r"[.!?:;…]$", s):
            s += "."
        lignes.append(s)
    t = " ".join(lignes)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)                 # links -> label
    t = re.sub(r"https?://\S+", "", t)                                # bare URLs
    t = re.sub(r"[*_~`]+", "", t)                                     # emphasis, inline code
    t = re.sub(r"[\U0001F000-\U0001FAFF☀-➿️]", "", t)  # emoji
    t = t.replace("→", ", ").replace("›", ", ").replace("·", ", ")
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > MAX:                                                  # cut at a sentence end
        coupe = max(t.rfind(p, 0, MAX) for p in (". ", "! ", "? "))
        t = t[: coupe + 1 if coupe > MAX // 2 else MAX]
    return t


def dernier_message(transcript: str) -> str:
    """Text of the last assistant turn in a Claude Code JSONL transcript."""
    morceaux = []
    for ligne in reversed(Path(transcript).read_text(encoding="utf-8").splitlines()):
        try:
            e = json.loads(ligne)
        except ValueError:
            continue
        if e.get("type") == "user" and not e.get("isMeta"):
            contenu = (e.get("message") or {}).get("content")
            if isinstance(contenu, str) or any(c.get("type") == "text" for c in contenu or []):
                break                                                 # previous user prompt
            continue                                                  # tool results
        if e.get("type") == "assistant":
            for c in reversed((e.get("message") or {}).get("content") or []):
                if c.get("type") == "text" and c.get("text", "").strip():
                    morceaux.append(c["text"])
            if morceaux:
                break                                                 # final text block of the turn
    return "\n".join(reversed(morceaux))


# ---------------------------------------------------------------- playback
def detacher(cmd):
    """Start `cmd` without blocking the agent; remember its pid to interrupt it."""
    arreter()
    opts: dict = {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    if WINDOWS:
        opts["creationflags"] = 0x00000008 | 0x00000200 | 0x08000000  # DETACHED, NEW_GROUP, NO_WINDOW
    else:
        opts["start_new_session"] = True
    p = subprocess.Popen(cmd, **opts)
    PID.write_text(str(p.pid))
    return p


def arreter():
    try:
        pid = int(PID.read_text())
    except (OSError, ValueError):
        return
    try:
        if WINDOWS:
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
        else:
            getattr(os, "killpg")(pid, signal.SIGTERM)
    except (OSError, ProcessLookupError):
        pass
    PID.unlink(missing_ok=True)


def temporaire(suffixe):
    fd, chemin = tempfile.mkstemp(suffix=suffixe)
    os.close(fd)
    return chemin


def fichier_texte(texte):
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8-sig" if WINDOWS else "utf-8")
    f.write(texte)
    f.close()
    return f.name


def powershell(script):
    return ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", script]


def jouer_audio(chemin):
    if WINDOWS:
        ps = ("Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; "
              f"$p.Open([uri]'{chemin}'); $i = 0; while (-not $p.NaturalDuration.HasTimeSpan -and $i -lt 50) "
              "{ Start-Sleep -Milliseconds 100; $i++ }; $p.Play(); "
              "Start-Sleep -Milliseconds ([int]$p.NaturalDuration.TimeSpan.TotalMilliseconds + 300); $p.Close()")
        return detacher(powershell(ps))
    for lecteur in (["afplay"], ["mpg123", "-q"], ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]):
        if shutil.which(lecteur[0]):
            return detacher(lecteur + [chemin])
    raise RuntimeError("aucun lecteur audio (afplay, mpg123, ffplay)")


# ---------------------------------------------------------------- engines
def piper(texte):
    modele = os.environ.get("ORAL_PIPER_MODEL")
    exe = shutil.which("piper")
    if not (modele and exe):
        raise RuntimeError("Piper non configuré (piper sur le PATH + ORAL_PIPER_MODEL)")
    wav = temporaire(".wav")
    subprocess.run([exe, "--model", modele, "--output_file", wav], input=texte.encode("utf-8"),
                   capture_output=True, check=True, timeout=120)
    if WINDOWS:
        return detacher(powershell(f"(New-Object Media.SoundPlayer '{wav}').PlaySync()"))
    return jouer_audio(wav)


def voix_systeme(texte):
    voix = os.environ.get("ORAL_VOICE", "")
    if WINDOWS:
        f = fichier_texte(texte)
        choix = (f"$s.SelectVoice('{voix.replace(chr(39), chr(39) * 2)}');" if voix else
                 "$v = $s.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture.Name -like 'fr*' } | "
                 "Select-Object -First 1; if ($v) { $s.SelectVoice($v.VoiceInfo.Name) };")
        ps = ("Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
              f"{choix} $s.Rate = {int(os.environ.get('ORAL_RATE', '1'))}; "
              f"$s.Speak([IO.File]::ReadAllText('{f}')); Remove-Item '{f}'")
        return detacher(powershell(ps))
    # The text goes through a file, never as an argument: a reply starting with "-" is not an option.
    if MAC:
        return detacher(["say"] + (["-v", voix] if voix else []) + ["-f", fichier_texte(texte)])
    if shutil.which("espeak-ng"):
        return detacher(["espeak-ng", "-v", voix or "fr", "-f", fichier_texte(texte)])
    if shutil.which("spd-say"):
        return detacher(["spd-say", "-w", "-l", "fr", "--", texte])
    raise RuntimeError("aucune voix système (spd-say, espeak-ng)")


def elevenlabs(texte):
    cle = os.environ.get("ELEVENLABS_API_KEY")
    if not cle:
        raise RuntimeError("ELEVENLABS_API_KEY absente")
    voix = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    corps = json.dumps({"text": texte, "model_id": os.environ.get("ELEVENLABS_MODEL", "eleven_flash_v2_5")})
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voix}?output_format=mp3_44100_64",
        data=corps.encode(), headers={"xi-api-key": cle, "Content-Type": "application/json"})
    # Corporate TLS inspection: trust the bundle the environment points at, never disable verification.
    ca = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    with urllib.request.urlopen(req, timeout=60, context=ssl.create_default_context(cafile=ca)) as r:
        mp3 = temporaire(".mp3")
        Path(mp3).write_bytes(r.read())
    return jouer_audio(mp3)


def parler(texte):
    if not texte:
        return
    force = os.environ.get("ORAL_ENGINE", "auto")
    moteurs = {"local": [piper, voix_systeme], "elevenlabs": [elevenlabs]}.get(force, [piper, voix_systeme, elevenlabs])
    erreurs = []
    for moteur in moteurs:
        try:
            p = moteur(texte)
            time.sleep(0.4)                                   # an engine that dies at once has failed
            if p is not None and p.poll() not in (None, 0):
                raise RuntimeError(f"code {p.returncode}")
            return moteur.__name__
        except Exception as e:  # noqa: BLE001  next engine
            erreurs.append(f"{moteur.__name__}: {e}")
    log("aucun moteur n'a parlé : " + " | ".join(erreurs))


# ---------------------------------------------------------------- entry points
def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    ETAT.mkdir(parents=True, exist_ok=True)
    if cmd == "on":
        DRAPEAU.touch()
        print("oral : activé")
        print("moteur :", parler("Mode oral activé.") or "aucun (voir ~/.claude/oral/oral.log)")
    elif cmd == "off":
        DRAPEAU.unlink(missing_ok=True)
        arreter()
        print("oral : désactivé")
    elif cmd == "status":
        print("oral :", "activé" if DRAPEAU.exists() else "désactivé")
    elif cmd == "stop":
        arreter()
    elif cmd in ("say", "test"):
        texte = " ".join(sys.argv[2:]) or "Essai de la voix du mode oral."
        print("moteur :", parler(nettoyer(texte)) or "aucun (voir ~/.claude/oral/oral.log)")
    elif cmd == "hook" and DRAPEAU.exists():
        entree = json.loads(sys.stdin.read() or "{}")
        texte = entree.get("last_assistant_message") or ""
        if not texte and entree.get("transcript_path"):
            texte = dernier_message(entree["transcript_path"])
        parler(nettoyer(texte))
    elif cmd == "codex" and DRAPEAU.exists():
        evt = json.loads(sys.argv[-1])
        if evt.get("type") == "agent-turn-complete":
            parler(nettoyer(evt.get("last-assistant-message") or ""))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001  a hook never breaks the session
        log(f"erreur : {e!r}")
