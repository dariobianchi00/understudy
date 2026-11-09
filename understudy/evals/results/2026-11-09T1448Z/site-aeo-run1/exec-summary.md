# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine could quote the three FAQ answers on about.html but could not attribute them to a named publisher, read the product's schema, or find a price.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 pages |
| llms.txt | absent |

## Top 3
1. **[P1] No Organization schema on any page** — no machine-readable publisher, logo or sameAs to attribute claims to (n/a)
2. **[P2] Homepage SoftwareApplication JSON-LD is invalid** — the only product schema is unparseable, `"price": }` (n/a)
3. **[P2] Pricing page gives no extractable price or plan answer** — nothing to quote for "what does it cost?" (n/a)

## Score
- **Score:** 4/10 — FAQ block is clean and quotable, but no Organization schema, broken product schema and no price leave most of the site unattributable.

## Limits on this read
- **Personas:** n/a — no-persona lens; run persona_mode is generic (⚠ INFERRED)
- **Not reached:** `/app/login.html` (robots), `features.html` (404), off-domain assets
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
None — no personas; a flip could not be observed.

## Next action
Add Organization JSON-LD site-wide and fix the homepage SoftwareApplication block.
