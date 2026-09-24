---
name: asset-brief
description: "Decide where each visual asset comes from and prepare it: open-source icon sets for UI icons, a ready-to-paste OpenAI Codex image prompt for illustrations, hero images, app icons and marketing visuals, then integrate the files (formats, sizes, favicon/PWA set, app icons). Use when a UI needs icons, images, illustrations, an app icon or a favicon. FR : « il me faut une illustration », « génère une image », « icône de l app », « favicon », « assets visuels »."
model: claude-opus-5-5
effort: low
---

# Asset brief

Follow `.claude/design-direction.md` or the project design system for style and palette.

## 1. Pick the source

| Asset | Source |
|---|---|
| UI icons | Open icon sets — Lucide, Phosphor, Tabler (MIT), Iconify MCP if present. Never generate. |
| Illustrations, hero images, empty-state art, textures, marketing visuals | Manual handoff to OpenAI Codex (image generation) |
| App icon | Codex for the artwork, then platform packaging (step 4) |
| Logos | Ask the user; never invent a brand mark |

## 2. Codex handoff

Claude cannot drive Codex. Output exactly this block, then wait:

> 👉 **Passe sur Codex et colle ce prompt.** Dépose les fichiers dans `<chemin>` puis dis « c'est fait ».

Prompt structure (one prompt per asset; for a set, reuse the same style anchor in each):

```
Use case: <where it appears, e.g. empty state of the invoices screen, mobile>
Subject: <what is shown, concrete>
Composition: <framing, focal point, safe margins, orientation>
Style anchor: <medium, rendering, line weight, lighting — identical across the set>
Palette: <hex values from design-direction>
Constraints: <no text | exact text "…">, transparent background (PNG), no watermark, no stock-photo look, no extra objects
Size: <e.g. 1536x1024 | 1024x1024 | 1024x1536>
Output file: <kebab-name>.png
```

## 3. Integrate

- Web: convert to WebP/AVIF, provide 1x/2x or `srcset`, keep SVG when vector, set explicit width/height, meaningful `alt` (empty for decorative).
- Favicon/PWA minimal set: `favicon.ico` (32), `icon.svg`, `apple-touch-icon.png` (180), `icon-192.png`, `icon-512.png`, maskable 512, `manifest.webmanifest`.
- iOS app icon: 1024×1024 master without rounded corners; layered `.icon` via Apple Icon Composer for Default / Dark / Clear / Tinted appearances.
- Android: adaptive icon (foreground + background layers, 108 dp with safe zone), monochrome layer for themed icons.
- Commit assets with the code that uses them.
