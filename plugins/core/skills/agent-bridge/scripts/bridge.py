#!/usr/bin/env python3
"""Share context, skills and MCP config between Claude Code and OpenAI Codex. Stdlib only.

Dry-run by default; add --apply to write. Run from the repo root.
  bridge.py context   AGENTS.md = shared source; CLAUDE.md imports it (@AGENTS.md) + Claude-only notes
  bridge.py skills    repo skills live in .agents/skills (Codex); .claude/skills/<name> links to them (Claude)
  bridge.py toolkit PATH   link every plugins/*/skills/* of a claude-toolkit clone into ~/.agents/skills (Codex)
  bridge.py mcp       print ~/.codex/config.toml entries equivalent to .mcp.json (review, then paste)
"""
import json, os, shutil, sys
from pathlib import Path

APPLY = "--apply" in sys.argv
args = [a for a in sys.argv[1:] if a != "--apply"]

def act(msg, fn=None):
    print(("APPLY  " if APPLY else "DRY    ") + msg)
    if APPLY and fn:
        fn()

def link(src: Path, dst: Path):
    if dst.exists() or dst.is_symlink():
        print(f"skip   {dst} (exists)")
        return
    def do():
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            dst.symlink_to(src.resolve(), target_is_directory=True)
        except OSError:  # Windows without symlink rights: copy instead
            shutil.copytree(src, dst)
    act(f"link   {dst} -> {src}", do)

def context():
    agents, claude = Path("AGENTS.md"), Path("CLAUDE.md")
    if not agents.exists() and claude.exists():
        body = claude.read_text(encoding="utf-8")
        act("create AGENTS.md from CLAUDE.md (shared, tool-neutral rules)", lambda: agents.write_text(body, encoding="utf-8"))
        act("rewrite CLAUDE.md as '@AGENTS.md' + Claude-only section",
            lambda: claude.write_text("@AGENTS.md\n\n## Claude Code only\n\n", encoding="utf-8"))
    elif agents.exists() and not claude.exists():
        act("create CLAUDE.md importing AGENTS.md", lambda: claude.write_text("@AGENTS.md\n\n## Claude Code only\n\n", encoding="utf-8"))
    elif agents.exists() and claude.exists():
        if "@AGENTS.md" not in claude.read_text(encoding="utf-8"):
            print("WARN   both files exist and CLAUDE.md does not import AGENTS.md: merge shared rules into AGENTS.md, then add '@AGENTS.md' at the top of CLAUDE.md")
        else:
            print("ok     CLAUDE.md imports AGENTS.md")
    else:
        act("create AGENTS.md + CLAUDE.md (@AGENTS.md)", lambda: (agents.write_text("# Project instructions\n\n", encoding="utf-8"),
                                                              claude.write_text("@AGENTS.md\n\n## Claude Code only\n\n", encoding="utf-8")))
    if Path("CLAUDE.local.md").exists():
        print("note   CLAUDE.local.md exists: fine here because CLAUDE.md imports AGENTS.md explicitly")

def skills():
    shared, claude = Path(".agents/skills"), Path(".claude/skills")
    if claude.is_dir():
        for d in claude.iterdir():
            if d.is_dir() and not d.is_symlink() and not (shared / d.name).exists():
                act(f"move   {d} -> {shared / d.name}", lambda d=d: (shared.mkdir(parents=True, exist_ok=True), shutil.move(str(d), shared / d.name)))
    if shared.is_dir() or not APPLY:
        for d in sorted(shared.iterdir()) if shared.is_dir() else []:
            if (d / "SKILL.md").exists():
                link(d, claude / d.name)

def toolkit(path):
    root = Path(path).expanduser()
    target = Path.home() / ".agents" / "skills"
    for skill in sorted(root.glob("plugins/*/skills/*/SKILL.md")):
        link(skill.parent, target / skill.parent.name)
    print("note   git pull in the clone updates Codex too (symlinks)")

def mcp():
    f = Path(".mcp.json")
    if not f.exists():
        print("no .mcp.json here")
        return
    for name, s in json.loads(f.read_text()).get("mcpServers", {}).items():
        print(f"\n[mcp_servers.{name}]")
        if "command" in s:
            print(f'command = "{s["command"]}"')
            print("args = " + json.dumps(s.get("args", [])))
        if "url" in s:
            print(f'url = "{s["url"]}"')
        if s.get("env"):
            print("env = { " + ", ".join(f'{k} = "{v}"' for k, v in s["env"].items()) + " }")

cmds = {"context": context, "skills": skills, "mcp": mcp}
if not args or args[0] not in (*cmds, "toolkit") or (args[0] == "toolkit" and len(args) < 2):
    print(__doc__)
    sys.exit(1)
toolkit(args[1]) if args[0] == "toolkit" else cmds[args[0]]()
