# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The pricing page is noindexed, the sitemap search engines are told to fetch 404s, and a nav link on every page leads to a dead 404 — a crawler can reach five pages but is actively told to drop the one that sells the product.

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — `/app/login.html` (disallowed by robots.txt), `analytics.example-tracker.test/t.js` (off-domain), `fonts.example-cdn.test/all.css` (off-domain)
- **Indexable:** 4 · **Blocked:** 1 (`/pricing.html`, `noindex`)

## Top 3
1. **[P0] Pricing page is noindexed** — the one page most likely to be searched for cannot appear in results (n/a)
2. **[P1] Nav "Features" link 404s on every page** — a link present in the header of all 5 crawled pages leads nowhere (n/a)
3. **[P1] About and Privacy pages share one non-descriptive title** — "Nimbus Notes" tells a search engine these two pages are the same thing (n/a)

## Score
- **Score:** 3/10 — a real page is hidden from search, the declared sitemap 404s, and a sitewide nav link is broken; the mechanics a crawler depends on are failing, not just polish.

## Limits on this read
- **Personas:** n/a — Mode C, no persona (generic crawl)
- **Not reached:** none beyond the 3 listed above (robots-disallowed and off-domain, both expected)
- **Excluded:** none in `scope_exclusions`
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — this lens has no persona, so a flip could not be observed.

## Next action
Remove `noindex` from `/pricing.html` and fix or publish `/sitemap.xml` before anything else on this list.
