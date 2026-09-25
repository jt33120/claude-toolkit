#!/usr/bin/env python3
"""Small dependency-free integrity check for the toolkit repository."""

import ast
import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_NAMES = {"core", "dev", "business"}
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid or missing JSON ({exc})")
        return {}


def frontmatter(path):
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", content, re.S)
    if not match:
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return None, None, content
    block = match.group(1)
    name = re.search(r"^name:\s*(\S+)\s*$", block, re.M)
    desc = re.search(r"^description:\s*(.*)$", block, re.M)
    if not name or not desc:
        errors.append(f"{path.relative_to(ROOT)}: missing name or description")
        return None, None, content
    raw = desc.group(1).strip()
    if raw in {">", "|"}:
        value = " ".join(line.strip() for line in block[desc.end():].splitlines() if line.strip())
    else:
        try:
            value = ast.literal_eval(raw) if raw.startswith(("'", '"')) else raw
        except (SyntaxError, ValueError):
            errors.append(f"{path.relative_to(ROOT)}: invalid description quoting")
            value = raw
    return name.group(1), value, content


def references(path, content):
    # Validate links and resource paths named in skill bodies, not remote URLs or globs.
    candidates = re.findall(r"\]\(([^)]+)\)", content)
    candidates += re.findall(r"`((?:references|scripts|templates|assets)/[^`]+)`", content)
    for candidate in candidates:
        target = unquote(candidate.split("#", 1)[0])
        if not target or re.match(r"\w+://", target) or target.startswith(("/", "#")):
            continue
        if any(c in target for c in "*{}<> ") or target.startswith(".") and target == ".":
            continue
        if not (path.parent / target).is_file():
            check(False, f"{path.relative_to(ROOT)}: missing reference {target}")


def validate():
    claude = load(ROOT / ".claude-plugin/marketplace.json")
    codex = load(ROOT / ".agents/plugins/marketplace.json")
    check(claude.get("name") == codex.get("name") == "claude-toolkit", "marketplace names differ")
    for catalog, portable in ((claude, False), (codex, True)):
        entries = catalog.get("plugins", [])
        check({e.get("name") for e in entries} == PLUGIN_NAMES, "marketplace entries differ from plugin folders")
        for entry in entries:
            name = entry.get("name")
            source = entry.get("source", {})
            target = source.get("path") if portable and isinstance(source, dict) else source
            check(target == f"./plugins/{name}" and (ROOT / str(target)).is_dir(),
                  f"marketplace path invalid for {name}")
            if portable:
                check(source.get("source") == "local", f"Codex catalog source invalid for {name}")

    names = set()
    skills = list(ROOT.glob("plugins/*/skills/*/SKILL.md"))
    check(bool(skills), "no skills found")
    for plugin in sorted(PLUGIN_NAMES):
        folder = ROOT / "plugins" / plugin
        old = load(folder / ".claude-plugin/plugin.json")
        new = load(folder / "plugin.json")
        check(new.get("$schema") == SCHEMA, f"{plugin}: portable plugin schema invalid")
        check(old.get("name") == new.get("name") == plugin, f"{plugin}: manifest name mismatch")
        check(old.get("version") == new.get("version") and bool(old.get("version")),
              f"{plugin}: manifest version mismatch")
        check(bool(old.get("description")) and bool(new.get("description")),
              f"{plugin}: empty manifest description")
    for skill in skills:
        name, description, content = frontmatter(skill)
        label = skill.relative_to(ROOT)
        check(name == skill.parent.name, f"{label}: name must match folder")
        check(name not in names, f"{label}: duplicate skill name")
        names.add(name)
        check(isinstance(description, str) and 0 < len(description) <= 1024,
              f"{label}: description must be 1–1024 characters")
        block = content.split("---", 2)[1] if content.startswith("---") else ""
        check(not re.search(r"^(?:model|effort):", block, re.M), f"{label}: model selection in frontmatter")
        references(skill, content)

    for agent in (ROOT / "plugins/dev/agents").glob("*.md"):
        block = agent.read_text(encoding="utf-8").split("---", 2)[1]
        check(not re.search(r"^(?:model|effort):", block, re.M), f"{agent.relative_to(ROOT)}: model selection")

    mcp = load(ROOT / "plugins/dev/mcp.json")
    legacy_mcp = load(ROOT / "plugins/dev/.mcp.json")
    check(mcp.get("$schema") == MCP_SCHEMA, "dev: portable MCP schema invalid")
    servers = mcp.get("mcpServers", {})
    check(set(servers) == set(legacy_mcp.get("mcpServers", {})), "dev: MCP server names differ")
    for name, server in servers.items():
        original = legacy_mcp.get("mcpServers", {}).get(name, {})
        check(server.get("type") == "stdio" and server.get("command") == original.get("command")
              and server.get("args") == original.get("args"), f"dev: MCP {name} differs from Claude config")

    directory = ROOT / "plugins/dev/skills/frontend-direction/references"
    check(not [p for p in directory.iterdir() if p.name.endswith((".tmp", ".part")) or "staging" in p.name.lower()],
          "frontend-direction: remove temporary or staging files after merging their data")
    with (directory / "styles.csv").open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    check(bool(rows) and len(rows[0]) == 29, "styles.csv: invalid header")
    check(all(len(row) == len(rows[0]) for row in rows[1:]), "styles.csv: inconsistent column count")
    try:
        ids = [int(row[0]) for row in rows[1:]]
    except (ValueError, IndexError):
        errors.append("styles.csv: invalid style ID")
        ids = []
    check(len(ids) == len(set(ids)), "styles.csv: duplicate style ID")
    check(set(range(1, 59)).union(range(71, 90)).issubset(ids),
          "styles.csv: missing consolidated style IDs")
    print("styles.csv: source gap 59–70 remains" if not set(range(59, 71)).intersection(ids) else
          "styles.csv: gap 59–70 has been partly or fully populated; review README")
    if errors:
        for issue in errors:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1
    print(f"Toolkit valid: {len(skills)} skills, {len(ids)} styles, 3 plugins")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
