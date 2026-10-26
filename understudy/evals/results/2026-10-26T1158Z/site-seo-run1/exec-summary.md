# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The pricing page is marked noindex and the nav links to a 404 features page, so search engines cannot index the page that matters most.

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed by robots.txt (/app/login.html), 2 off-domain
- **Indexable:** 3 · **Blocked:** 2 (pricing noindex; features 404)

## Top 3
1. **[P0] Pricing page is noindex** — the pricing page cannot appear in search (n/a)
2. **[P1] Nav link to /features.html returns 404** — dead end on all 5 pages (n/a)
3. **[P1] About and privacy share the title "Nimbus Notes"** — duplicate titles merge the two pages (n/a)

## Score
- **Score:** 4/10 — pricing is hidden from search and the nav has a dead link; the rest of the site is crawlable

## Limits on this read
- **Personas:** n/a — crawl-only lens; manifest persona_mode generic
- **Not reached:** /app/ (robots disallow), sitemap contents (404)
- **Excluded:** none; auth wall not scored
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — no persona; a flip could not be observed.

## Next action
Remove the noindex tag from pricing.html, then fix the Features link.
