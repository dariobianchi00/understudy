# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The pricing page is deliberately hidden from search engines, the primary nav points at a 404 on every page, and the declared sitemap does not exist — a crawler that respects robots.txt gets none of the site's real content map.

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed by robots.txt (`/app/login.html`), 2 off-domain (analytics/font CDN)
- **Indexable:** 4 (`/`, `/about.html`, `/privacy.html`, and `/features.html` only as a 404) · **Blocked:** 1 (`/pricing.html`, `noindex`)

## Top 3
1. **[P0] Pricing page is noindexed** — the one page a search visitor would search for cannot rank (n/a)
2. **[P1] Primary nav links to a 404 page on every crawled page** — every page sends crawlers and users to `/features.html`, which does not exist (n/a)
3. **[P2] Declared sitemap returns 404** — robots.txt points crawlers at a sitemap that has 0 reachable URLs (n/a)

## Score
- **Score:** 3/10 — the site's most commercially important page is invisible to search, and its own sitemap is broken

## Limits on this read
- **Personas:** n/a — SEO is scored from crawl records, not persona traversal
- **Not reached:** `/app/login.html` (robots-disallowed, correctly excluded)
- **Excluded:** auth wall (`/app/login.html`) — infrastructure, not scored
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — no persona ran in this lens.

## Next action
Remove `noindex` from `/pricing.html` and fix or repoint the site-wide `/features.html` nav link.
