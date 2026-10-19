# Nimbus Notes — aeo — Run 2026-10-19 (fixture01)

An answer engine could quote the three FAQ answers on /about.html, but could not attribute them to any declared organisation, and every other page offers nothing extractable.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 (1 valid; homepage JSON-LD invalid) |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 pages |
| llms.txt | absent |

## Top 3
1. **[P1] No Organization schema on any crawled page** — nothing declares name, url, logo or sameAs, so attribution has no anchor (n/a)
2. **[P2] Homepage JSON-LD is invalid** — the only product schema fails to parse, so no product facts are machine-readable (n/a)
3. **[P2] Pricing page states no price** — "Pricing depends on your workspace type and sync topology." leaves nothing to quote (n/a)

## Score
- **Score:** 4/10 — one clean FAQ page, but no organisation identity, broken homepage schema, and no quotable pricing or product definition

## Limits on this read
- **Personas:** n/a — static-markup lens, no persona judgement
- **Not reached:** /app/login.html (robots.txt disallow); two off-domain assets; /features.html returned 404
- **Excluded:** none in manifest; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`
- **Not measured:** live answer-engine behaviour, current citation (out of v1 scope)

## Numbers
Not applicable — no persona timings in this lens.

## Severity flips
None — lens has no personas, so a flip could not be observed.

## Next action
Add a sitewide Organization JSON-LD block and repair the homepage SoftwareApplication JSON-LD.
