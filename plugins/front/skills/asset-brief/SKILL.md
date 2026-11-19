---
name: asset-brief
description: "Choose and prepare visual assets: open-source icon sets, ready-to-paste image prompts for illustrations, hero images and app icons, then integrate formats and the favicon/PWA set. FR : « il me faut une illustration », « icône de l'app », « favicon »."
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
