# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The site is technically crawlable but tells search engines not to index the one page that answers what it costs, and points its own primary navigation at a page that 404s.

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed (`/app/login.html`, robots.txt `/app/`), 2 off-domain (analytics script, font CDN)
- **Indexable:** 3 (`/`, `/about.html`, `/privacy.html`) · **Blocked:** 1 noindex (`/pricing.html`), 1 broken (`/features.html`, 404)

## Top 3
1. **[P0] Pricing page carries `noindex`** — the only page that answers "what does it cost" cannot appear in search results at all (n/a)
2. **[P1] Declared sitemap 404s** — `sitemap.xml` from robots.txt resolves to nothing, so crawlers get no authoritative URL list (n/a)
3. **[P1] Primary nav links to `/features.html` on every crawled page, and it 404s** — every page, including itself, points at a dead Features page (n/a)

## Score
- **Score:** 3/10 — a P0 (pricing hidden from search) plus a broken sitemap and a site-wide dead nav link outweigh otherwise-clean basics (lang, charset, one H1 on most pages, valid FAQ schema).

## Limits on this read
- **Personas:** n/a — SEO is a crawl-only lens, no persona ran. ⚠ Run-level `persona_mode` is `generic` for other lenses.
- **Not reached:** none beyond the not-crawled list above.
- **Excluded:** none (`scope_exclusions` is empty). `/app/login.html` is the auth wall — infrastructure, not scored.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
No persona flow applies to this lens. See **Crawl coverage** above for the equivalent figures (pages found, crawled, indexable, blocked).

## Severity flips
None observed — no persona ran, so a flip could not be observed.

## Next action
Remove the `noindex` from `/pricing.html` and fix the `/features.html` link (restore the page or repoint the nav) before anything else on this list.
