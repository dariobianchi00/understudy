# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The site is technically crawlable, but its pricing page is noindexed, its main navigation links to a 404 on every page, and its sitemap is broken — a search engine can reach the site but cannot fully index or trust it.

## Crawl coverage
- **Pages crawled:** 5 of 6 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed by robots.txt (`/app/login.html`), 2 off-domain assets (analytics script, font CDN — not pages)
- **Indexable:** 3 · **Blocked:** 2 (pricing.html — noindex; features.html — 404)

## Top 3
1. **[P0] Pricing page is noindexed, blocking it from search results** — the one page a cost-focused search would need can never rank (n/a)
2. **[P1] Primary nav links to /features.html on every page, which 404s** — every crawled page burns crawl budget and link equity on a dead end (n/a)
3. **[P2] Declared sitemap returns 404 and cannot be crawled** — no sitemap-based discovery or freshness signal reaches this site (n/a)

## Score
- **Score:** 4/10 — a real, page-blocking indexability fault (noindexed pricing) plus a sitewide broken nav link cap what would otherwise be a clean, well-linked small site.

## Limits on this read
- **Personas:** n/a — this lens scores from the crawl record only, no persona (`persona_mode: generic` on the run, not applicable to this lens)
- **Not reached:** none beyond the disallowed/off-domain items listed above — crawl cap (15) was not exhausted
- **Excluded:** `/app/login.html` (robots.txt disallow — auth wall, infrastructure)
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a (crawl-only lens) | n/a | n/a | n/a | n/a |

## Severity flips
None — this lens has no personas, so a flip cannot be observed.

## Next action
Remove `noindex` from pricing.html and fix or delink /features.html before anything else on this list.
