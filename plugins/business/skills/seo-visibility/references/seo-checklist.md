# SEO and AI visibility — checklist and reference

## Keyword research

Assess for each opportunity: primary vs. secondary, search-volume signal (high/med/low), difficulty (easy/mod/hard), long-tail and question-based variants ("how to", "what is"), intent (informational/navigational/commercial/transactional). Include 15-25 opportunities sorted by opportunity score (demand x relevance / difficulty) in the final table:

| Keyword | Est. Difficulty | Opportunity | Current Ranking | Intent | Recommended Content |

## On-page checklist

- Title tag: unique, ≤60 chars, primary keyword
- Meta description: ≤160 chars, includes keyword + CTA
- Exactly one H1 per page, matching the title tag's intent
- H2/H3 hierarchy uses secondary keywords naturally
- Primary keyword in first 100 words, used naturally (no stuffing)
- Internal links: 2-3 to related pages, descriptive anchor text
- Image alt text descriptive, keyword where relevant
- Clean URL slugs

| Page | Issue | Severity (Critical/High/Medium/Low) | Fix |

## Technical checklist

| Check | Status (Pass/Fail/Warning) | Details |
|---|---|---|
| Page speed | | large images, render-blocking scripts, redirect chains |
| Mobile-friendliness | | responsive layout, tap targets, viewport |
| Structured data | | FAQ, Product/SoftwareApplication, Organization schema present |
| robots.txt / sitemap.xml | | present, accurate, not accidentally blocking crawlers |
| Broken links | | internal/external 404s, redirect chains |
| HTTPS | | secure, no mixed content |
| Indexation | | pages that should be indexed but aren't; duplicate content |

## Content gap analysis

For each gap: topic/keyword, why it matters (demand + competitor coverage + funnel stage), recommended format, priority, effort (quick win <2h / moderate half-day / substantial multi-day).

## Impact/effort scoring for prioritization

Rank by impact, not ease. Usual SaaS order: crawler access → renderability → fact accuracy → structured data → llms.txt → off-site listings → content rewrites → link building.

**Quick wins (this week):** fix title tags, add meta descriptions, unblock AI crawlers in robots.txt, fix broken links, add alt text.
**Strategic (this quarter):** topic cluster / pillar page, llms.txt + schema rollout, off-site listing claims, content overhaul.

## llms.txt minimal template

```
# [Product Name]

> [One-sentence description of what the product does and who it's for]

## Product
[2-3 sentences: core features, pricing model]

## Contact
[support email / contact page URL]

## Key pages
- Pricing: [url]
- Docs: [url]
```

## robots.txt — allow AI crawlers (example additions)

```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /
```

## Schema.org starter (SoftwareApplication)

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "[Product]",
  "applicationCategory": "BusinessApplication",
  "offers": {"@type": "Offer", "price": "[price]", "priceCurrency": "EUR"}
}
```

## Competitor comparison table

| Dimension | Your Site | Competitor A | Competitor B | Winner |
|---|---|---|---|---|
| Keyword count / overlap | | | | |
| Content depth | | | | |
| Publishing frequency | | | | |
| Backlink signals | | | | |
| Technical score | | | | |
| AI-answer presence | | | | |
