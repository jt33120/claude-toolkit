---
name: diagrams
description: "Draw architecture, workflow, sequence, ER and state diagrams as code (Mermaid by default, D2 for polished visuals, LikeC4 for a queryable C4 model), versioned next to the code and validated before commit. Use when a doc, PRD, architecture, PR or README needs a diagram, or when an existing diagram must follow a code change. FR : « fais un schéma », « diagramme d'architecture », « diagramme de séquence », « schéma du workflow », « modèle de données », « mets à jour le schéma »."
---

# Diagrams as code

The source (`.mmd`, `.d2`, `.c4`, or a ```` ```mermaid ```` block) is the diagram; images are build outputs. Diagrams live with the docs they explain (BMAD architecture, `docs/`, README) and change in the same PR as the code they describe.

## 1. Pick the tool

| Need | Tool | Rendering |
|---|---|---|
| Default: flow, sequence, ER, state, class, Gantt, small architecture | Mermaid, inline in the Markdown doc | GitHub, GitLab and VS Code render it natively: no image to commit |
| Diagram for a client, a deck or a decision-maker, where layout and look matter | D2 (`.d2` → SVG) | `d2` CLI |
| Many services, several deployments, questions like "what depends on Postgres?" | LikeC4 model (`.c4`), one model → many C4 views | `likec4` CLI, optional MCP |

Start with Mermaid. Move to D2 only for a visual deliverable, to LikeC4 only when the system has roughly 5+ containers or several environments and diagrams start drifting from each other. PlantUML and Python Diagrams are not used here: a JVM or Graphviz dependency for little gain.

## 2. Write it

- One diagram, one question (who calls whom, what happens on login, where data lives). Split rather than cram; aim for under ~15 nodes.
- Name nodes with the project's real terms (services, tables, routes); label edges with the protocol or action.
- Mermaid: put the diagram in the doc that explains it; a standalone `docs/diagrams/<name>.mmd` only when several docs reuse it.
- LikeC4: one model in `docs/architecture/*.c4`; views are derived, never copied. Before writing the DSL, install its official skill: `npx skills add likec4/likec4 --skill likec4-dsl -a claude-code -y` *(verify)*. `npx likec4 gen mermaid -o docs/diagrams` produces Mermaid views GitHub can render.

## 3. Validate before commit

- Mermaid: `npx -y @mermaid-js/mermaid-cli -i <file>.mmd -o /tmp/<file>.svg` (or extract the block to a temp `.mmd`). A parse error exits non-zero. In a cloud session, reuse the installed Chromium: `PUPPETEER_SKIP_DOWNLOAD=1` and `-p puppeteer.json` containing `{"executablePath": "<chromium path>", "args": ["--no-sandbox"]}`.
- D2: `d2 fmt <file>.d2` then `d2 <file>.d2 <file>.svg` (install: `go install oss.terrastruct.com/d2@latest` or the official script). Use the free layout engines (dagre, elk); TALA is paid.
- LikeC4: `npx likec4 validate [dir]`; export with `npx likec4 export png -o docs/render [dir]`.
- Read the rendered SVG/PNG once: overlapping labels or a spaghetti layout mean split or reorder.

Commit rendered images only when they are consumed outside GitHub (deck, PDF, client doc), next to their source, regenerated in the same commit.

## 4. MCP (optional)

- LikeC4 MCP (`npx likec4 mcp docs/architecture`, stdio) lets the agent query the model; add it to the project's `.mcp.json` once a LikeC4 model exists.
- The official Mermaid MCP (`https://mcp.mermaid.ai/mcp`) is remote and needs a Mermaid account: diagrams leave the machine. Not needed for writing or validating Mermaid; never use it for client or confidential architectures.
