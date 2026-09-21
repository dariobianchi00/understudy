# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine could extract almost nothing cleanly from this site: Organization schema is absent everywhere, the homepage's only JSON-LD is broken, and four of the five crawled pages carry zero question-shaped content — only the About page gives an engine anything it could quote and attribute.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 (1 invalid) |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 page |
| llms.txt | absent |

## Top 3
1. **[P1] No Organization schema anywhere; entity identity exists only in prose** — an engine has no machine-readable way to confirm who Nimbus Notes is (n/a)
2. **[P1] Homepage's only JSON-LD is invalid and unparsable** — the sole structured description of the product fails to parse at all (n/a)
3. **[P1] Four of five crawled pages have zero extractable answer blocks** — including the pricing page, which states no price anywhere (n/a)

## Score
- **Score:** 4/10 — one page (About) is genuinely extractable; everything else — the homepage's product schema, the pricing page, entity identity — gives an answer engine nothing clean to quote.

## Limits on this read
- **Personas:** n/a — this lens has no persona mode; findings rest on crawl evidence only.
- **Not reached:** `/app/login.html` (excluded — auth wall/robots), off-domain analytics and font CDN requests.
- **Excluded:** auth wall (`/app/login.html`, disallowed by robots.txt) — infrastructure, not scored.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
None — this lens carries no personas, so a flip could not be observed.

## Next action
Add a site-wide Organization block and fix the homepage's truncated SoftwareApplication JSON-LD first — both are foundational and cheap relative to their extraction impact.
