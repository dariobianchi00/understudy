# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The pricing page is blocked from search by noindex, and a 404 nav link plus a dead, wrong-host sitemap undermine crawling of an otherwise small, clean site.

## Top 3
1. **[P0] Pricing page is noindex, so it cannot appear in search** — the cost page can never be found via search (n/a)
2. **[P1] Every page links to /features.html, which returns 404** — nav dead-ends on all 5 pages (n/a)
3. **[P1] Declared sitemap returns 404 and points at a different host** — crawlers get no URL list (n/a)

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed (/app/), 2 off-domain
- **Indexable:** 3 · **Blocked:** 2 (pricing noindex, login disallowed); the 404 is also not indexable

## Score
- **Score:** 4/10 — the pricing page is excluded from search and the sitemap and a main nav link are broken; the rest is polish.

## Limits on this read
- **Personas:** n/a — ⚠ INFERRED (generic); crawl-based lens
- **Not reached:** /app/login.html (robots disallow); off-domain assets
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
- None — no personas in this lens, so a flip could not be observed.

## Next action
- Remove noindex from /pricing.html, then fix /features.html and publish the sitemap.
