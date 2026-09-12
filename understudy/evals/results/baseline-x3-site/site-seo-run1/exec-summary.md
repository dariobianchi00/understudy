# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

A crawler can reach and read most of this site, but a noindex tag hides the pricing page and a dead nav link points at a 404 from every page, so what does get indexed is a thinner, more confusing picture of the product than it should be.

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — `/app/login.html` (disallowed by robots.txt), `analytics.example-tracker.test/t.js` and `fonts.example-cdn.test/all.css` (off-domain)
- **Indexable:** 4 (`/`, `/about.html`, `/privacy.html`, `/features.html`'s 404 aside) · **Blocked:** 1 (`/pricing.html`, `noindex`)

## Top 3
1. **[P0] Pricing page is noindex, removing it from search results** — the one page a searcher comparing plans would want to find is invisible to search engines (n/a)
2. **[P1] Main navigation links to /features.html on every page, which 404s** — every crawl of every page hits a dead end in primary nav, wasting crawl budget and signalling neglect (n/a)
3. **[P1] Declared sitemap returns 404** — the site tells search engines where its sitemap is, then serves nothing there, so there is no machine-readable page list to fall back on (n/a)

## Score
- **Score:** 4/10 — a crawler can index the site, but a P0 noindex on a core page plus a dead sitemap and a broken nav link mean what gets indexed and found is unreliable.

## Limits on this read
- **Personas:** n/a — SEO is scored from crawl records only, no persona involved.
- **Not reached:** none beyond the not-crawled list above (disallowed and off-domain items, both expected).
- **Excluded:** `/app/login.html` — auth wall, not reported as a finding.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — this lens has no personas, so a flip could not be observed.

## Next action
Remove `noindex` from `/pricing.html`, fix the sitemap at the declared URL, and repoint or remove the `/features.html` nav link.
