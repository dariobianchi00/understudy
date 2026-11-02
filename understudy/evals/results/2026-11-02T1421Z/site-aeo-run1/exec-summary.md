# Nimbus Notes — aeo — Run 2026-11-02 (fixture01)

An answer engine could cleanly quote exactly one page of this site (the About FAQ) and could not attribute any of it, because no Organization schema exists and the home page's only JSON-LD is broken.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 (1 valid) |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 pages |
| llms.txt | absent |

## Top 3
1. **[P1] No Organization schema on any page** — publisher cannot be attributed from markup (n/a)
2. **[P2] Home JSON-LD is invalid** — the main page has zero usable structured data (n/a)
3. **[P2] Pricing page states no prices** — no cost answer can be lifted (n/a)

## Score
- **Score:** 4/10 — one good FAQ page; everywhere else nothing to quote, no publisher identity in markup.

## Limits on this read
- **Personas:** n/a — no-persona lens, static crawl only
- **Not reached:** /app/login.html (robots.txt), 2 off-domain assets; /features.html returned 404
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
None — no persona lens.

## Next action
Add a valid Organization JSON-LD block (name, url, logo, sameAs) to every page and repair the home page JSON-LD.
