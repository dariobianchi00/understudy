# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

A search engine can reach every page from the homepage, but the pricing page is noindexed, the site's declared sitemap 404s, and the primary nav links to a features page that also 404s on every page of the site.

## Crawl coverage
- **Pages crawled:** 5 of 5 found · depth `standard`
- **Not crawled:** 3 — disallowed (`/app/login.html`, per robots.txt), off-domain (analytics tracker script, font CDN stylesheet)
- **Indexable:** 3 · **Blocked:** 1 (noindex) — plus 1 page returning 404 (`/features.html`)

## Top 3
1. **[P0] Pricing page is noindexed, blocking cost information from search results** — the page that answers "what does it cost" cannot appear in search at all (n/a)
2. **[P1] Declared sitemap returns 404 and lists zero URLs** — search engines follow the site's own signal to an error (n/a)
3. **[P1] Global nav links to /features.html, which returns a 404 on every page** — every crawl of the site's nav dead-ends (n/a)

## Score
- **Score:** 4/10 — the entry page is clean and crawlable, but the page most tied to the stated buyer objective is hidden from search, and the site's own sitemap and nav contradict it.

## Limits on this read
- **Personas:** n/a — Mode C, crawl-only lens, no persona invoked
- **Not reached:** `/app/login.html` — disallowed by robots.txt, auth wall
- **Excluded:** none in manifest's `scope_exclusions`; the auth wall above is never reported per standing rule
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
N/A — this lens has no personas; see **Crawl coverage** above for the equivalent figures.

## Severity flips
None — single crawl, no personas to flip across.

## Next action
Remove the `noindex` from pricing.html and publish a working sitemap; both are one-line fixes with outsized reach.
