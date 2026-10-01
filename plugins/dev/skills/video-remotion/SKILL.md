---
name: video-remotion
description: "Edit and render videos as code with Remotion (React): reels and shorts 9:16, product demos, motion design, animated captions, intros/outros, montage of existing clips, free stock B-roll (Pexels, Pixabay). Installs the official Remotion agent skills, scaffolds the project, previews in Remotion Studio and renders MP4. Use when the user wants to cut, assemble, animate or subtitle a video. FR : « montage vidéo », « fais un reel », « monte ces rushes », « sous-titres animés », « vidéo de démo », « B-roll », « vidéos libres de droits », « Remotion »."
---

# Video with Remotion

Remotion turns React components into frames, then encodes MP4/WebM/GIF. Claude writes the composition; the user approves in Studio before the final render.

## 1. Brief (ask only what is missing)

- Output: platform, ratio and size (reel/short 1080×1920, YouTube 1920×1080, square 1080×1080), fps (30 default), target duration.
- Sources: rushes, music, logos, fonts, text/script. Files go in `public/` and are loaded with `staticFile()`.
- Style: follow `.claude/design-direction.md` or the brand palette when present.
- Images to create (thumbnails, illustrations): route through `asset-brief`.

## 2. Setup (once per project)

- New project: `npx create-video@latest` (blank template unless one fits).
- Official skills, loaded before writing any composition: `npx skills add remotion-dev/skills -a claude-code -y` (Codex: `-a codex`). They hold the up-to-date API rules; follow them over this file. The old `remotion-documentation` MCP is retired in favour of these skills.
- Requires Node; rendering downloads a headless Chrome on first run.

## 3. Build

- One `<Composition>` per deliverable in `src/Root.tsx`; variants (ratios, languages) share components and differ by props.
- Rushes: `<OffthreadVideo>` trimmed with `trimBefore` + `durationInFrames` (`startFrom`/`endAt` are deprecated), sequenced with `<Series>` or `<Sequence>`; transitions via `@remotion/transitions`.
- Every animation derives from `useCurrentFrame()` (`interpolate`, `spring`); never CSS animations or `setTimeout`.
- Captions: transcribe with `@remotion/install-whisper-cpp` (local, free), display with `@remotion/captions`; keep text inside the platform safe zone (reels: avoid the bottom ~20 % and right edge).

## 4. B-roll (stock footage beyond screen recordings)

Free sources, commercial use allowed. Keys are free (account on pexels.com and pixabay.com) and read from `PEXELS_API_KEY` / `PIXABAY_API_KEY`; never print or commit them. If a key is missing, say which one and where to create it, then continue with the other source or the user's own rushes.

1. Plan shots first: for each scene write 2–3 concrete search terms in English (e.g. "hands typing laptop night", "aerial coastal road").
2. Search: `python scripts/broll.py search "<terms>" --orientation portrait --min-duration 4` (omit `--orientation` for landscape). Output is JSON: pick by duration, resolution and page title, never by the first hit; open `page_url` if unsure.
3. Download only the chosen clips: `python scripts/broll.py download <pexels|pixabay> <id> --out public/broll`. Each file is logged in `public/broll/credits.json` (source page, author, license).
4. Montage: load with `staticFile("broll/<file>")` in `<OffthreadVideo muted>`; use `objectFit: "cover"` to fill the frame, trim to the useful 2–5 s, keep the audio from the user's music/voice-over only.
5. Credits: Pexels asks to credit the author and link to Pexels. Put a line in the video description (or an end card) built from `credits.json`, and give it to the user with the render.
6. Not allowed: recognizable people in a misleading context, implying endorsement by anyone shown, or reselling the clips as stock. Clips from other sources (Wikimedia Commons, Internet Archive, NASA) are handled manually: record the exact license and author in `credits.json` and respect its attribution terms (CC BY, CC BY-SA, etc.).
7. Heavy clips: add `public/broll/*.mp4` to `.gitignore` and commit `credits.json` only.

## 5. Check, then render

1. `npx remotion studio` — the user reviews and asks for changes there.
2. Spot-check key frames without a full render: `npx remotion still <id> out/frame.png --frame=<n>`.
3. Final: `npx remotion render <id> out/<name>.mp4` (add `--crf` for quality/size trade-off). Report path, duration, size and resolution.
4. Do not commit renders or heavy rushes; add `out/` to `.gitignore`.

## Licenses

Stock clips: see step 4. Remotion itself:

Free for individuals, non-profits and companies up to 3 employees, commercial use included. Beyond that, a Remotion company license is required — say so before starting if the user's organisation may exceed it.
