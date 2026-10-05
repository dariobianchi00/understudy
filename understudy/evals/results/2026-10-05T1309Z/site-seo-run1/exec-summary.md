# Nimbus Notes — seo — Run 2026-09-08 (fixture01)

The pricing page tells search engines not to index it, and the sitemap, structured data and nav links all contradict what the site wants found.

## Crawl coverage
- **Pages crawled:** 5 of 6 found · depth `standard`
- **Not crawled:** 3 — 1 disallowed by robots.txt (`/app/login.html`), 2 off-domain (tracker script, font CSS); none over cap or timed out
- **Indexable:** 3 · **Blocked:** 2 (pricing `noindex`; `/app/` disallowed)

## Top 3
1. **[P0] Pricing page is noindex, so search engines are told to drop it** — a page that should rank is removed from the index (n/a)
2. **[P1] Features page returns 404 yet is linked from the nav on every page** — 5 of 5 crawled pages link to a dead URL (n/a)
3. **[P1] Home page JSON-LD is invalid and cannot be parsed** — entry page's structured data is ignored (n/a)

## Score
- **Score:** 5/10 — a `noindex` on the pricing page caps the score; titles, descriptions and headings are also weak, though the entry page is crawlable.

## Limits on this read
- **Personas:** n/a — crawl-only lens; `persona_mode` is generic, so findings rest on inferred personas — ⚠ INFERRED (generic)
- **Not reached:** `/app/login.html` (robots-disallowed); no sitemap URLs to check (sitemap 404)
- **Excluded:** none in scope exclusions; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`
- **Not checked:** rankings, traffic, keywords, backlinks — a crawl holds no such data

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a (crawl) | n/a | n/a | n/a | n/a |

## Severity flips
- None — Mode C has no persona, so a flip could not be observed.

## Next action
- Remove the `noindex` meta tag from `/pricing.html`, then fix the dead `features.html` link.
