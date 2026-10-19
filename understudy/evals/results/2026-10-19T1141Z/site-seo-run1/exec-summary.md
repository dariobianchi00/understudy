# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The pricing page is marked noindex and the declared sitemap is a 404, so search engines can neither see the page that matters most nor get a URL list.

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed by robots.txt (/app/), 2 off-domain
- **Indexable:** 3 · **Blocked:** 2 (pricing noindex; features 404)

## Top 3
1. **[P0] Pricing page is noindex and will be dropped from search results** — pricing cannot be found in search (n/a)
2. **[P1] Features page returns 404 yet is linked from every page** — crawlers hit a dead end on all 5 pages (n/a)
3. **[P1] Declared sitemap returns 404 and points to a different host** — no URL list for search engines (n/a)

## Score
- **Score:** 4/10 — the pricing page is excluded from the index, a main-nav page 404s, and the sitemap is missing.

## Limits on this read
- **Personas:** n/a — crawl-only lens, no persona (persona_mode generic)
- **Not reached:** /app/login.html (robots-disallowed); 2 off-domain resources
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Check | Result |
|---|---|
| Findings | 1 P0 · 2 P1 · 3 P2 · 2 P3 |
| Pages with unique title and description | 1 of 5 |

## Severity flips
None — no personas, so a flip could not be observed.

## Next action
- Remove noindex from pricing.html, restore or unlink /features.html, and publish a sitemap on the production host.
