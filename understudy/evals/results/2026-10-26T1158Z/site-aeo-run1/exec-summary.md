# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine could cleanly quote exactly one page of this site (the About FAQ) and could not attribute any of it to a machine-readable organisation.

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
1. **[P1] No Organization schema on any of 5 crawled pages** — nothing machine-readable says who publishes Nimbus Notes (n/a)
2. **[P1] Home-page JSON-LD is invalid** — the only product schema fails to parse, so it is ignored (n/a)
3. **[P2] FAQPage schema lists 2 of the 3 visible FAQ answers** — the data-residency answer is not in the markup (n/a)

## Score
- **Score:** 4/10 — one good FAQ page; identity schema missing, product schema broken, pricing and home page unquotable

## Limits on this read
- **Personas:** n/a — no-persona lens, static markup only. `persona_mode` is generic; persona-based findings elsewhere rest on INFERRED personas.
- **Not reached:** /app/login.html (robots.txt disallow), 2 off-domain assets; /features.html returned 404
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Next action
Fix the home-page JSON-LD, add an Organization block with sameAs, then put prices and question headings on the pricing and home pages.
