#!/usr/bin/env python3
"""Share project instructions and skills between Claude Code and Codex.

Run from the target project root. Read-only by default; --apply enables safe writes.
  context         Create or import AGENTS.md without discarding existing CLAUDE.md text.
  skills          Copy existing Claude skills into .agents/skills and link new shared skills.
  toolkit PATH    Link toolkit skills into the local Codex skills directory.
  mcp             Print Codex TOML for .mcp.json without printing credential values.
This local bridge does not install plugins in ChatGPT Work or Codex cloud.
"""
import hashlib
import json
import os
import re
import shutil
import sys
import uuid
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

APPLY = False
MARKER = ".agent-bridge-source.json"


def act(message, fn=None):
    print(("APPLY  " if APPLY else "DRY    ") + message)
    if APPLY and fn:
        fn()


def digest(directory: Path) -> str:
    """Hash file paths and bytes so a locally edited copy cannot be overwritten."""
    result = hashlib.sha256()
    for item in sorted(directory.rglob("*")):
        if not item.is_file() or item.name == MARKER:
            continue
        result.update(item.relative_to(directory).as_posix().encode("utf-8"))
        result.update(b"\0")
        result.update(item.read_bytes())
        result.update(b"\0")
    return result.hexdigest()


def write_copy(src: Path, dst: Path):
    shutil.copytree(src, dst)
    (dst / MARKER).write_text(
        json.dumps({"source": str(src.resolve()), "digest": digest(src)}) + "\n",
        encoding="utf-8",
    )


def refresh_copy(src: Path, dst: Path):
    temporary = dst.with_name(dst.name + ".bridge-new-" + uuid.uuid4().hex)
    backup = dst.with_name(dst.name + ".bridge-old-" + uuid.uuid4().hex)
    try:
        write_copy(src, temporary)
        os.replace(dst, backup)
        try:
            os.replace(temporary, dst)
        except OSError:
            os.replace(backup, dst)
            raise
        shutil.rmtree(backup)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)


def link(src: Path, dst: Path):
    src = src.resolve()
    if not (src / "SKILL.md").is_file():
        print(f"WARN   missing SKILL.md: {src}")
        return
    if dst.is_symlink():
        if dst.resolve() == src:
            print(f"ok     linked {dst}")
        else:
            print(f"WARN   {dst} points elsewhere; leaving it untouched")
        return
    if dst.exists():
        marker = dst / MARKER
        if not dst.is_dir() or not marker.is_file():
            print(f"WARN   {dst} exists without a bridge marker; leaving it untouched")
            return
        try:
            state = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            print(f"WARN   invalid bridge marker at {dst}; leaving it untouched")
            return
        if state.get("source") != str(src) or state.get("digest") != digest(dst):
            print(f"WARN   {dst} has local changes or another source; leaving it untouched")
            return
        if state["digest"] != digest(src):
            act(f"refresh copied skill {dst}", lambda: refresh_copy(src, dst))
        else:
            print(f"ok     copied skill {dst} is current")
        return

    def create():
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            dst.symlink_to(src, target_is_directory=True)
        except OSError:
            # On Windows without symlink privileges, keep a tracked copy that can refresh.
            write_copy(src, dst)

    act(f"link or copy {dst} <- {src}", create)


def context():
    agents, claude = Path("AGENTS.md"), Path("CLAUDE.md")
    if claude.is_symlink():
        print("WARN   CLAUDE.md is a symlink; review its target manually before migrating")
        return
    if claude.exists() and not agents.exists():
        print("WARN   CLAUDE.md exists but AGENTS.md does not. Keep CLAUDE.md intact; "
              "manually move only shared rules into AGENTS.md, then rerun context.")
    elif agents.exists() and claude.exists():
        current = claude.read_text(encoding="utf-8")
        if any(line.strip() == "@AGENTS.md" for line in current.splitlines()):
            print("ok     CLAUDE.md imports AGENTS.md")
        else:
            # Prepend, never rewrite or discard existing Claude-only content.
            act("prepend @AGENTS.md to CLAUDE.md (all existing content retained)",
                lambda: claude.write_text("@AGENTS.md\n\n" + current, encoding="utf-8"))
    elif agents.exists():
        act("create CLAUDE.md importing AGENTS.md",
            lambda: claude.write_text("@AGENTS.md\n\n## Claude Code only\n\n", encoding="utf-8"))
    else:
        act("create AGENTS.md and CLAUDE.md",
            lambda: (agents.write_text("# Project instructions\n\n", encoding="utf-8"),
                     claude.write_text("@AGENTS.md\n\n## Claude Code only\n\n", encoding="utf-8")))
    if Path("CLAUDE.local.md").exists():
        print("note   CLAUDE.local.md exists; keep project imports explicit")


def skills():
    shared, claude = Path(".agents/skills"), Path(".claude/skills")
    if claude.is_dir():
        for source in sorted(claude.iterdir()):
            destination = shared / source.name
            if source.is_dir() and not source.is_symlink() and (source / "SKILL.md").is_file() and not destination.exists():
                act(f"copy {source} -> {destination} (original retained)",
                    lambda s=source, d=destination: (d.parent.mkdir(parents=True, exist_ok=True),
                                                      shutil.copytree(s, d)))
                print(f"note   Review both copies of {source.name}; retire the original only after confirming the shared skill")
    if shared.is_dir():
        for source in sorted(shared.iterdir()):
            if (source / "SKILL.md").is_file():
                link(source, claude / source.name)


def toolkit(path):
    root = Path(path).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Toolkit directory not found: {root}")
    target = Path.home() / ".agents" / "skills"
    found = sorted(root.glob("plugins/*/skills/*/SKILL.md"))
    if not found:
        raise SystemExit(f"No toolkit skills found in: {root}")
    names = [path.parent.name for path in found]
    if len(names) != len(set(names)):
        raise SystemExit("Duplicate skill names across toolkit plugins: choose unique names first")
    for skill in found:
        link(skill.parent, target / skill.parent.name)
    print("note   Run toolkit again after updates to refresh Windows copies; "
          "local links update automatically. Cloud hosts need their own plugin installation.")


def mcp():
    config = Path(".mcp.json")
    if not config.is_file():
        print("no .mcp.json in the project")
        return
    servers = json.loads(config.read_text(encoding="utf-8")).get("mcpServers", {})
    for name, server in servers.items():
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
            print(f"WARN   server name requires manual TOML escaping: {name!r}")
            continue
        url = server.get("url")
        if url:
            parsed = urlsplit(url)
            secret_query = any(re.search(r"token|secret|key|password|auth|credential", key, re.I)
                               for key, _ in parse_qsl(parsed.query))
            if parsed.username or parsed.password or secret_query:
                print(f"WARN   {name}: credential in URL; configure manually without exposing it")
                continue
        if "command" not in server and not url:
            print(f"WARN   {name}: no supported command or URL")
            continue
        command_args = server.get("args", [])
        if any(re.search(r"(?:--?(?:token|secret|password|api[-_]?key|auth)(?:=|$)|sk-[A-Za-z0-9]{20,})", str(arg), re.I)
               for arg in [server.get("command", ""), *command_args]):
            print(f"WARN   {name}: possible literal credential in command/args; configure manually")
            continue
        names = sorted(server.get("env", {}))
        if not all(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key) for key in names):
            print(f"WARN   {name}: review invalid environment variable names manually")
            continue
        print(f"\n[mcp_servers.{name}]")
        if "command" in server:
            print("command = " + json.dumps(server["command"], ensure_ascii=False))
            print("args = " + json.dumps(command_args, ensure_ascii=False))
        else:
            print("url = " + json.dumps(url, ensure_ascii=False))
        if names and "command" in server:
            print("env_vars = " + json.dumps(names, ensure_ascii=False))
            print(f"# Set these environment variables in Codex before connecting {name}; values intentionally omitted.")
        elif names:
            print(f"# Review HTTP authentication for {name} manually; credential values omitted.")


def main(argv=None):
    global APPLY
    args = sys.argv[1:] if argv is None else argv
    APPLY = "--apply" in args
    args = [a for a in args if a != "--apply"]
    commands = {"context": context, "skills": skills, "mcp": mcp}
    if not args or args[0] not in (*commands, "toolkit") or len(args) != (2 if args[0] == "toolkit" else 1):
        print(__doc__)
        raise SystemExit(1)
    toolkit(args[1]) if args[0] == "toolkit" else commands[args[0]]()


if __name__ == "__main__":
    main()
