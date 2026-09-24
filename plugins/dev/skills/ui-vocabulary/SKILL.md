---
name: ui-vocabulary
description: >
  EN: Reference for finding the exact technical name of a UI component or
  pattern, its variants/states, cross-platform equivalents (web, iOS,
  Android), and alternatives — so you stop defaulting to the same solution.
  Use for "what is this component called", "what's the right component
  for...", "alternatives to a modal", "exhaustive list of options for...",
  "UI vocabulary", naming things precisely in a design or dev spec, or
  picking between several valid UI patterns.
  FR: Référence pour trouver le nom technique exact d'un composant ou motif
  d'interface, ses variantes/états, ses équivalents multi-plateformes (web,
  iOS, Android), et des alternatives — pour éviter de toujours proposer la
  même solution. Utiliser pour "comment s'appelle ce composant", "quel
  composant pour...", "alternatives à une modale", "vocabulaire UI", "liste
  exhaustive des options pour...", ou pour nommer précisément un élément
  d'interface dans un brief ou une spec.
model: claude-opus-5-5
effort: low
---

# UI Vocabulary

A naming and options reference for UI components and UX patterns. It is a
dictionary, not a style guide: it never argues for one look over another.

## What this is NOT

This skill does not recommend a visual style, spacing, color, or "best"
component. It has no aesthetic opinions. Its only job is vocabulary and
options. **The project's design system, brand guidelines, and platform
conventions always win** — if the project already has a pattern for this,
use that pattern's name and shape, not a suggestion from here.

## How to use it

1. **Find by intent.** Start from what the user is trying to do (navigate,
   input a value, confirm a choice, show status, display data, lay out a
   screen, add motion, or a higher-level UX flow) and open the matching
   reference file below.
2. **Pick 2–4 candidates**, not one answer. Read the "Use when" / "Avoid
   when" columns to shortlist rather than default to the first or most
   familiar name.
3. **Check the platform note.** Web, iOS, and Android often have different
   idiomatic names and controls for the same idea (e.g. bottom sheet vs.
   action sheet vs. modal bottom sheet). Match the target platform's own
   vocabulary — do not force a web term onto a native app or vice versa.
4. **Offer alternatives, never impose.** When asked "what component should
   I use", present the shortlist with trade-offs and let the user or the
   project's existing design system decide. Do not silently pick one.
5. **Use exact names in specs.** When writing a brief, ticket, or handoff,
   prefer the precise term (and its "also called" synonyms) over vague
   language like "popup" or "box".

## Reference index (`references/`)

| File | Covers |
|---|---|
| `navigation.md` | Tabs, nav bars, sidebars, breadcrumbs, pagination, steppers, drawers, command palettes, menus |
| `inputs.md` | Text fields, selects, pickers, sliders, search, tag input, file upload, rating |
| `selection.md` | Checkboxes, radios, switches, toggle groups, chips, listboxes, multi-select |
| `overlays.md` | Dialogs, sheets, drawers, popovers, tooltips, menus, action sheets, toasts |
| `feedback.md` | Toasts, banners, alerts, progress, skeletons, empty/error states, badges |
| `data-display.md` | Tables, lists, cards, accordions, trees, timelines, avatars, carousels, calendars |
| `layout.md` | Containers, grids, stacks, split views, sticky headers, safe areas, dividers |
| `media-and-motion.md` | Images, video, galleries, icons; transitions, gestures, easing vocabulary |
| `patterns.md` | Higher-level UX patterns: onboarding, wizards, undo, infinite scroll, search/filter/sort, auth, paywalls |

Each table's columns: **Name · Also called · What it is · Use when · Avoid
when · Variants/states · Web (HTML/ARIA, shadcn/Radix) · iOS (SwiftUI) ·
Android (Compose/Material) · Alternatives.**

## Sources (names and concepts only — no text copied)

- component.gallery — https://component.gallery/
- Open UI — https://open-ui.org/
- Material 3 components — https://m3.material.io/components
- Apple Human Interface Guidelines — https://developer.apple.com/design/human-interface-guidelines/
- shadcn/ui — https://ui.shadcn.com/docs/components
- Radix Primitives — https://www.radix-ui.com/primitives — Base UI — https://base-ui.com/
- React Aria — https://react-spectrum.adobe.com/react-aria/
- SwiftUI views — https://developer.apple.com/documentation/swiftui/
- Jetpack Compose / Material components — https://developer.android.com/jetpack/compose
- ui-patterns.com — https://ui-patterns.com/
