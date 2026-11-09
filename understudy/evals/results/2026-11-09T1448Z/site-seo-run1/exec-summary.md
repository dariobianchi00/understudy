# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The pricing page is marked noindex and the declared sitemap and the features page both 404, so search engines cannot properly find or index this site.

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed (/app/login.html), 2 off-domain
- **Indexable:** 3 · **Blocked:** 1 noindex (pricing); features is a 404

## Top 3
1. **[P0] Pricing page carries noindex and is hidden from search** — the cost page will be dropped from results (n/a)
2. **[P1] Features page returns 404 while linked from all 5 pages** — dead nav link on every page (n/a)
3. **[P1] Declared sitemap returns 404** — crawlers get no URL list (n/a)

## Score
- **Score:** 3/10 — a key commercial page is noindexed and sitemap and features URLs are dead

## Limits on this read
- **Personas:** n/a — no-persona lens; persona_mode generic (⚠ INFERRED personas, unused here)
- **Not reached:** /app/login.html (robots disallow); off-domain assets
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — no personas on this lens.

## Next action
Remove noindex from pricing.html, then fix the features URL and sitemap.
