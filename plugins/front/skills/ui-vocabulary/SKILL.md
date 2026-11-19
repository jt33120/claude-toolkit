---
name: ui-vocabulary
description: "Find the exact name of a UI component or pattern, its states, web/iOS/Android equivalents and alternatives. Use to name things precisely in a spec or to choose between patterns. FR : « comment s'appelle ce composant », « alternatives à une modale »."
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
