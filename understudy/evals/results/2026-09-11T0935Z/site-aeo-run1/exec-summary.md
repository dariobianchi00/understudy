# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine could extract almost nothing reliable from this site's static markup: no valid Organization schema exists anywhere, the homepage's only JSON-LD block is malformed, and 3 of the 5 crawled pages carry zero extractable answer content.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 page (of 5 crawled) |
| llms.txt | absent |

## Top 3
1. **[P1] No Organization schema anywhere on the site** — a machine has to parse About-page prose to learn who this company is; nothing declares it in structured data (n/a)
2. **[P1] Homepage only structured data is invalid JSON-LD** — the entry page's sole schema block fails to parse, so it yields nothing to an extractor (n/a)
3. **[P2] Home, pricing and privacy pages have zero extractable answer blocks** — 3 of 5 crawled pages have no question-shaped content to lift out and quote (n/a)

## Score
- **Score:** 4/10 — the one page with real Q&A content (About) is only half marked up, everything else is either broken schema or un-structured marketing prose.

## Limits on this read
- **Personas:** n/a — AEO scores static markup extractability, not persona flows. (Run's `persona_mode` is `generic`, per manifest.json, but that setting does not affect this lens.)
- **Not reached:** `/app/login.html` (disallowed by robots.txt `/app/`) · off-domain analytics/font assets (out of crawl domain)
- **Excluded:** none declared in `manifest.json` (`scope_exclusions: []`)
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
n/a — this lens has no personas, so a severity flip cannot occur.

## Next action
Fix the homepage's JSON-LD, add a site-wide Organization block from the About page's existing facts, and complete the About page's FAQPage markup.
