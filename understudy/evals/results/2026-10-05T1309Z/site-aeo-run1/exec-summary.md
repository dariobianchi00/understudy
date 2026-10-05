# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine could quote the three FAQ answers on /about.html and nothing else: no Organization schema, a broken homepage JSON-LD, no price anywhere, and no llms.txt.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 (1 of the 2 invalid) |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 page |
| llms.txt | absent |

## Top 3
1. **[P1] No Organization schema on any page** — publisher name, logo and sameAs cannot be attributed from markup (n/a)
2. **[P1] Homepage JSON-LD is invalid JSON** — the only SoftwareApplication declaration is discarded by parsers (n/a)
3. **[P2] Pricing page states no price** — "what does Nimbus Notes cost" has no quotable answer (n/a)

## Score
- **Score:** 4/10 — one clean FAQ page works, but publisher identity, product schema and pricing cannot be extracted.

## Limits on this read
- **Personas:** n/a — no-persona lens; `persona_mode` is generic (⚠ INFERRED) but this lens does not use personas
- **Not reached:** /features.html (404), /app/login.html (disallowed by robots.txt /app/), two off-domain assets
- **Excluded:** none; auth wall not reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — no personas in this lens.

## Next action
Add one valid Organization JSON-LD block (name, url, logo, sameAs) site-wide and fix the homepage JSON-LD.
