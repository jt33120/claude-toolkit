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
PLUGIN_NAMES = {"core", "dev", "front", "media", "business"}
# Descriptions are loaded in every session; business is only installed for management work.
MAX_DESCRIPTION = {"business": 1024}
DEFAULT_MAX_DESCRIPTION = 300
SKILL_REF = re.compile(r"(?<![\w./@-])/?(" + "|".join(sorted(PLUGIN_NAMES)) + r"):([a-z0-9][a-z0-9-]*)")
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
        resolved = (path.parent / target).resolve()
        if not resolved.is_file():
            check(False, f"{path.relative_to(ROOT)}: missing reference {target}")
        # Each plugin is installed in its own folder, so links into another plugin break at runtime.
        plugin_root = ROOT / "plugins" / path.relative_to(ROOT).parts[1]
        if path.is_relative_to(ROOT / "plugins") and not resolved.is_relative_to(plugin_root) \
                and not resolved.is_relative_to(ROOT / "licenses"):
            check(False, f"{path.relative_to(ROOT)}: reference {target} leaves its plugin")


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
        check(bool(old.get("description")) and old.get("description") == new.get("description"),
              f"{plugin}: manifest descriptions empty or different")
    entries = {e.get("name"): e for e in claude.get("plugins", [])}
    for plugin in sorted(PLUGIN_NAMES):
        manifest = load(ROOT / "plugins" / plugin / ".claude-plugin/plugin.json")
        check(entries.get(plugin, {}).get("description") == manifest.get("description"),
              f"{plugin}: marketplace description differs from manifest")

    owners = {}
    for skill in skills:
        name, description, content = frontmatter(skill)
        label = skill.relative_to(ROOT)
        plugin = skill.parts[-4]
        limit = MAX_DESCRIPTION.get(plugin, DEFAULT_MAX_DESCRIPTION)
        check(name == skill.parent.name, f"{label}: name must match folder")
        check(name not in names, f"{label}: duplicate skill name")
        names.add(name)
        owners[name] = plugin
        check(isinstance(description, str) and 0 < len(description) <= limit,
              f"{label}: description must be 1–{limit} characters")
        block = content.split("---", 2)[1] if content.startswith("---") else ""
        check(not re.search(r"^(?:model|effort):", block, re.M), f"{label}: model selection in frontmatter")
        references(skill, content)

    for agent in ROOT.glob("plugins/*/agents/*.md"):
        name, description, content = frontmatter(agent)
        label = agent.relative_to(ROOT)
        block = content.split("---", 2)[1] if content.startswith("---") else ""
        check(not re.search(r"^(?:model|effort):", block, re.M), f"{label}: model selection")
        check(isinstance(description, str) and 0 < len(description) <= DEFAULT_MAX_DESCRIPTION,
              f"{label}: description must be 1–{DEFAULT_MAX_DESCRIPTION} characters")

    # Namespaced calls such as `/front:distill` must name a skill of that plugin.
    docs = [p for p in ROOT.glob("**/*") if p.is_file() and ".git" not in p.parts
            and p.suffix in {".md", ".json", ".snippet", ".yaml", ".py", ".sh"}]
    for doc in docs:
        for plugin, skill in SKILL_REF.findall(doc.read_text(encoding="utf-8", errors="ignore")):
            check(owners.get(skill) == plugin,
                  f"{doc.relative_to(ROOT)}: {plugin}:{skill} does not name a skill of {plugin}")

    for plugin in sorted(PLUGIN_NAMES):
        folder = ROOT / "plugins" / plugin
        if not ((folder / ".mcp.json").exists() or (folder / "mcp.json").exists()):
            continue
        mcp = load(folder / "mcp.json")
        legacy_mcp = load(folder / ".mcp.json")
        check(mcp.get("$schema") == MCP_SCHEMA, f"{plugin}: portable MCP schema invalid")
        servers = mcp.get("mcpServers", {})
        check(set(servers) == set(legacy_mcp.get("mcpServers", {})), f"{plugin}: MCP server names differ")
        for name, server in servers.items():
            original = legacy_mcp.get("mcpServers", {}).get(name, {})
            check(server.get("type") == "stdio" and server.get("command") == original.get("command")
                  and server.get("args") == original.get("args"), f"{plugin}: MCP {name} differs from Claude config")
            check(not any("@latest" in str(arg) for arg in server.get("args", [])),
                  f"{plugin}: MCP {name} must pin a version, not @latest")

    directory = ROOT / "plugins/front/skills/frontend-direction/references"
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
    print(f"Toolkit valid: {len(skills)} skills, {len(ids)} styles, {len(PLUGIN_NAMES)} plugins")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
