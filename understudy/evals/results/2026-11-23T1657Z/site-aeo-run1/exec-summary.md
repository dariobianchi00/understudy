# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine could quote the three FAQ answers on /about.html but could not attribute them to a declared organisation, parse the homepage's broken schema, or find any price.

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
1. **[P1] No Organization schema on any crawled page** — publisher facts exist only as prose on /about.html (n/a)
2. **[P1] Homepage JSON-LD is invalid (empty price value)** — the only product schema is unparseable (n/a)
3. **[P2] Pricing page states no price and carries no Offer schema** — cost cannot be extracted (n/a)

## Score
- **Score:** 5/10 — one clean FAQ page, but no Organization, broken homepage schema, no price, no category sentence

## Limits on this read
- **Personas:** none used by this lens; run persona_mode is generic — ⚠ INFERRED
- **Not reached:** /app/login.html (robots.txt), 2 off-domain assets; /features.html is a 404
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — this lens has no personas, so a flip could not be observed.

## Next action
Add Organization JSON-LD and repair the homepage block, then publish a price on /pricing.html.
