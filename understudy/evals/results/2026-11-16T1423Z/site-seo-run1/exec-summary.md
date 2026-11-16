# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The pricing page is marked noindex and the declared sitemap returns 404, so the pages a buyer would search for are hidden or undiscoverable.

## Top 3
1. **[P0] Pricing page is noindex, so it cannot be indexed** — the page that answers "what does it cost" is removed from search (n/a)
2. **[P1] Declared sitemap returns 404 and points to a different host** — crawlers have no sitemap to work from (n/a)
3. **[P1] Internal link /features.html returns 404 from all 5 crawled pages** — the nav on every page links to a dead end (n/a)

## Score
- **Score:** 4/10 — a noindexed pricing page, no working sitemap, and a nav link that 404s on every page

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed by robots.txt (/app/login.html), 2 off-domain
- **Indexable:** 3 · **Blocked:** 2 (pricing noindex, features 404)

## Limits on this read
- **Personas:** n/a — crawl lens; persona_mode generic
- **Not reached:** sitemap contents (404); JS-rendered content not checked
- **Excluded:** none; auth wall not reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — no personas in a crawl lens, so a flip could not be observed.

## Next action
Remove noindex from pricing.html, then publish a sitemap and fix the /features.html link.
