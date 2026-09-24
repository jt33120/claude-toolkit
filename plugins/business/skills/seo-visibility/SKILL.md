---
name: seo-visibility
description: "Audits and improves both halves of being found online: classic SEO (keywords, on-page, technical, content gaps, competitor comparison) and AI-answer visibility (crawler access, llms.txt, schema.org, whether ChatGPT/Perplexity/Claude cite the site). Works on any public site with no connector, from a URL. Use for SEO audit, keyword research, technical SEO, AI search visibility, GEO, AEO, being found on Google, showing up in ChatGPT, référencement, visibilité SEO, visibilité IA, audit technique, mots-clés."
model: claude-opus-5-5
effort: medium
---

<!--
Provenance: merged and condensed from anthropics/knowledge-work-plugins (Apache-2.0):
marketing/skills/seo-audit, small-business/skills/seo-ai-visibility.
Connector-specific (Wix/Shopify write-path, SEO-tool) boilerplate removed; kept tool-agnostic —
runs by crawling the public site directly, no connector required.
-->

# SEO and AI Visibility

Makes a small SaaS site findable by search engines and by AI assistants, using open standards only. This skill never tries to influence what an assistant recommends — it only makes a site easier to read, crawl, and quote accurately. Say that plainly if asked; refuse hidden text, fake reviews, prompt injection in pages, or fabricated credentials even if requested.

## Step 1 — Crawl and gather

No connector needed — fetch the site directly. Cover: homepage, pricing, key feature/landing pages, blog, about, contact; `robots.txt`, `sitemap.xml`, `llms.txt`; what renders in raw HTML vs. what needs JavaScript (many SPAs hide content from crawlers — check this first, it is usually the highest-impact SaaS-specific issue); titles, meta descriptions, heading structure, alt text, internal links; existing structured data; page speed/mobile signals. Say what was crawled and what could not be reached (behind login, broken, etc.).

If the user supplies keyword-tool or analytics exports, cross-reference; otherwise use web research and say precision is limited without a connected SEO tool.

## Step 2 — Classic SEO audit

Run through `references/seo-checklist.md`: keyword opportunities (primary/secondary/long-tail, intent), on-page issues (title/meta/H1/alt/internal linking), content gaps vs. 2-3 likely competitors, technical checklist (speed, mobile, structured data, crawlability, HTTPS, broken links).

## Step 3 — AI visibility audit

This is usually what the founder actually means by "why don't we show up in AI answers."

1. **Crawler access** — does `robots.txt` allow ClaudeBot, GPTBot, PerplexityBot and peers? A blanket block (common on SaaS sites behind Cloudflare/security plugins) is the single highest-impact, one-line fix.
2. **Renderability** — if content only appears after JS runs, most crawlers see an empty page.
3. **llms.txt** — a plain-language file at the root: what the product does, who it's for, pricing model, how to reach the company.
4. **Structured data** — schema.org SoftwareApplication/Product/FAQPage/Organization so facts are machine-readable, not inferred.
5. **Fact clarity** — pricing tiers, what the product does, who it's for stated plainly and consistently in one place. Vague or contradictory facts get quoted wrong.
6. **Off-site presence** — G2/Capterra-style listings, directories, review platforms assistants read from.

## Step 4 — Test what an assistant actually sees

Ask a few real prospect questions ("what's a good tool for X") in different phrasings and record what comes back — whether the product appears, who does, what was cited. State plainly this varies run to run and is not a ranking; a monthly repeat shows direction, one run proves little. Never report a "visibility score."

## Step 5 — Score, prioritize, and write the fixes

Score each finding on impact vs. effort (table in `references/seo-checklist.md`). Give the 5 that matter, not 40. Usual order: unblock crawlers → fix renderability → correct facts → add structured data → publish llms.txt → claim listings → rewrite content.

Produce actual files/copy, not just advice: corrected `robots.txt`, an `llms.txt` draft, ready-to-paste JSON-LD blocks, rewritten titles/meta descriptions, and rewritten page copy that answers real prospect questions. Route any customer-facing copy through **writing-voice** and **language-strategy** before finalizing — get the EN/FR mix right for the target market. DNS-level fixes (TXT/CNAME records) are handed back as exact record instructions, never applied directly — a wrong DNS change can take a site offline.

Never invent a claim, credential, or customer count the founder has not stated.

## Step 6 — Deliver and set a recheck

Give a priority table, the copy-paste fixes, and a recheck date — 30 days minimum before a change shows up; say so plainly.

## What not to do

- Never frame this as influencing what an AI recommends — it is crawlability and accuracy only.
- No hidden text, cloaking, keyword stuffing, fake reviews, or embedded instructions to AI systems.
- Never fabricate facts to fill schema or content.
- Never report a fake "AI visibility score."

## Reference files

- `references/seo-checklist.md` — full crawl checklist, keyword/on-page/technical tables, impact-effort scoring, llms.txt and schema templates.
