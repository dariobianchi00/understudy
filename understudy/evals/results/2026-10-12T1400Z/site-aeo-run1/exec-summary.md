# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine could quote Nimbus Notes' about-page FAQ cleanly, but could not tell who publishes the site, what category it is in, or what it costs.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 (1 valid, 1 invalid) |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 pages |
| llms.txt | absent |

## Top 3
1. **[P1] No Organization schema on any of 5 crawled pages** — publisher facts exist only as prose on /about.html (n/a)
2. **[P2] Homepage JSON-LD is invalid** — the sole product schema is unparseable (n/a)
3. **[P2] Pricing page states no prices or plan facts** — cost questions have nothing to quote (n/a)

## Score
- **Score:** 5/10 — one clean FAQ page, but no publisher identity, broken product schema, and no quotable pricing or category.

## Limits on this read
- **Personas:** n/a — no-persona lens; run `persona_mode` is generic
- **Not reached:** /app/login.html (robots.txt disallow); /features.html returned 404
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
None — no persona dimension in this lens.

## Next action
Add a sitewide Organization JSON-LD block, then repair the homepage JSON-LD.
