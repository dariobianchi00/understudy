# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The site is crawlable, but the pricing page is set to noindex, the Features nav link is a 404, and the sitemap is missing.

## Top 3
1. **[P0] Pricing page is noindex** — /pricing.html will be dropped from search results (n/a)
2. **[P1] /features.html returns 404 from all 5 pages** — every crawl follows a dead nav link (n/a)
3. **[P2] Sitemap declared but 404** — no sitemap for crawlers to discover pages from (n/a)

## Crawl coverage
- **Pages crawled:** 5 of 6 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed (/app/login.html) · 2 off-domain
- **Indexable:** 3 · **Blocked:** 2 (pricing noindex; login robots-disallowed)

## Score
- **Score:** 5/10 — Site is crawlable, but the pricing page is noindex and the Features nav link is dead.

## Limits on this read
- **Personas:** n/a — crawl-only lens; persona_mode generic ⚠ INFERRED
- **Not reached:** /app/login.html (robots), off-domain assets
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — crawl lens, no personas.

## Next action
- Remove noindex from pricing.html, then fix the /features.html link.
