# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The pricing page — the one page the objective depends on — is set `noindex`, the declared sitemap 404s, and every page's global nav points at a Features page that also 404s.

## Top 3
1. **[P0] Pricing page is noindexed, hiding it from search results** — the commercial page a searcher would need is invisible to search engines by explicit instruction (n/a)
2. **[P1] Global navigation links to a Features page that 404s** — every crawled page sends crawlers (and visitors) into a dead end from primary nav (n/a)
3. **[P2] Declared sitemap returns 404** — robots.txt points crawlers at a sitemap that does not exist, so the site's own discovery aid is broken (n/a)

## Score
- **Score:** 3/10 — a page-1 blocker (noindexed pricing) plus a sitewide broken nav link and a dead sitemap outweigh otherwise-clean basics (lang, charset, robots.txt present)

## Limits on this read
- **Personas:** n/a — Mode C, no persona (`persona_mode: generic` applies to the other lenses in this run, not this one)
- **Not reached:** nothing beyond the 3 URLs robots.txt/off-domain rules excluded — see Crawl coverage
- **Excluded:** none recorded in `manifest.json` scope_exclusions
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — disallowed by robots.txt (`/app/login.html`), off-domain (analytics tracker script, font CDN stylesheet)
- **Indexable:** 3 (`/`, `/about.html`, `/privacy.html`) · **Blocked:** 2 (`/pricing.html` — noindex, `/features.html` — 404)

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — this lens has no personas, a flip cannot be observed.

## Next action
Remove `noindex` from `/pricing.html`, fix or restore `/features.html`, and republish a working `sitemap.xml` at the declared URL.
