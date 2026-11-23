# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The pricing page is marked noindex, the sitemap 404s, and the nav links a 404 features page, so a crawler can reach little of the commercially important content.

## Top 3
1. **[P0] Pricing page is noindex** — the cost page cannot appear in search (n/a)
2. **[P1] Declared sitemap returns 404, on a different host** — crawlers get no URL list (n/a)
3. **[P1] Features page 404s, linked from all 5 pages** — dead end in every nav (n/a)

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed by robots.txt (/app/), 2 off-domain
- **Indexable:** 3 · **Blocked:** 1 noindex (pricing) + 1 404 (features)

## Score
- **Score:** 4/10 — the pricing page is noindexed and the sitemap is dead; the rest is metadata polish

## Limits on this read
- **Personas:** n/a — crawl lens, no persona (persona_mode generic)
- **Not reached:** /app/ (robots-disallowed), off-domain assets
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
- None — no persona ran for this lens, so a flip could not be observed.

## Next action
- Remove noindex from pricing.html and publish a working sitemap.
