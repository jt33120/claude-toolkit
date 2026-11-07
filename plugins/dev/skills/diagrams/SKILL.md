---
name: diagrams
description: "Draw architecture, workflow, sequence, ER and state diagrams as code (Mermaid by default, Diagram Design for polished deliverables, LikeC4 for a queryable C4 model), versioned next to the code and validated before commit. Use when a doc, PRD, architecture, PR or README needs a diagram, or when an existing diagram must follow a code change. FR : « fais un schéma », « diagramme d'architecture », « diagramme de séquence », « schéma du workflow », « modèle de données », « mets à jour le schéma »."
---

# Diagrams as code

The source (`.mmd`, `.c4`, a Diagram Design HTML file, or a ```` ```mermaid ```` block) is the diagram; images are build outputs. Diagrams live with the docs they explain (BMAD architecture, `docs/`, README) and change in the same PR as the code they describe.

## 1. Pick the tool

| Need | Tool | Rendering |
|---|---|---|
| Default: flow, sequence, ER, state, class, Gantt, small architecture | Mermaid, inline in the Markdown doc | GitHub, GitLab and VS Code render it natively: no image to commit |
| Diagram for a client, a deck or a decision-maker, where layout and look matter | Diagram Design: 45 diagram types as self-contained HTML/SVG, brand style guide, imports Mermaid | Its own skill: `npx skills add cathrynlavery/diagram-design` (MIT) |
| Many services, several deployments, questions like "what depends on Postgres?" | LikeC4 model (`.c4`), one model → many C4 views | `likec4` CLI, optional MCP |

Start with Mermaid. Move to Diagram Design only for a visual deliverable (set its style guide to the project's brand on first use; it can start from the existing Mermaid), to LikeC4 only when the system has roughly 5+ containers or several environments and diagrams start drifting from each other. For a deliverable whose every box must be traced to the code (architecture review, before/after on a large PR), Archify (`npx skills add tt-a1i/archify`, Apache-2.0) validates nodes against repository evidence; heavier, use it only for that. PlantUML, D2 and Python Diagrams are not used here.

## 2. Write it

- One diagram, one question (who calls whom, what happens on login, where data lives). Split rather than cram; aim for under ~15 nodes.
- Name nodes with the project's real terms (services, tables, routes); label edges with the protocol or action.
- Mermaid: put the diagram in the doc that explains it; a standalone `docs/diagrams/<name>.mmd` only when several docs reuse it.
- LikeC4: one model in `docs/architecture/*.c4`; views are derived, never copied. Before writing the DSL, install its official skill: `npx skills add likec4/likec4 --skill likec4-dsl -a claude-code -y` *(verify)*. `npx likec4 gen mermaid -o docs/diagrams` produces Mermaid views GitHub can render.

## 3. Validate before commit

- Mermaid: `npx -y @mermaid-js/mermaid-cli -i <file>.mmd -o /tmp/<file>.svg` (or extract the block to a temp `.mmd`). A parse error exits non-zero. In a cloud session, reuse the installed Chromium: `PUPPETEER_SKIP_DOWNLOAD=1` and `-p puppeteer.json` containing `{"executablePath": "<chromium path>", "args": ["--no-sandbox"]}`.
- Diagram Design: open the HTML in a browser once (or screenshot it with Playwright) and export SVG/PNG with its own export step.
- LikeC4: `npx likec4 validate [dir]`; export with `npx likec4 export png -o docs/render [dir]`.
- Read the rendered SVG/PNG once: overlapping labels or a spaghetti layout mean split or reorder.

Commit rendered images only when they are consumed outside GitHub (deck, PDF, client doc), next to their source, regenerated in the same commit.

## 4. MCP (optional)

- LikeC4 MCP (`npx likec4 mcp docs/architecture`, stdio) lets the agent query the model; add it to the project's `.mcp.json` once a LikeC4 model exists.
- The official Mermaid MCP (`https://mcp.mermaid.ai/mcp`) is remote and needs a Mermaid account: diagrams leave the machine. Not needed for writing or validating Mermaid; never use it for client or confidential architectures.
