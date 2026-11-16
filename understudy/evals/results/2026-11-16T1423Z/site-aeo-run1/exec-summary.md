# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine could cleanly quote the three FAQ answers on /about.html, but nothing else: there is no Organization schema, the homepage's only JSON-LD is broken, and pricing and homepage offer nothing quotable.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 (1 of the 2 is invalid) |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 pages |
| llms.txt | absent |

## Top 3
1. **[P1] No Organization schema anywhere on the site** — nothing machine-readable says who publishes Nimbus Notes (n/a)
2. **[P2] Homepage SoftwareApplication JSON-LD is invalid and unparseable** — the homepage's only structured data yields nothing (n/a)
3. **[P2] Homepage and pricing have zero extractable answer blocks** — no question headings and no price stated on /pricing.html (n/a)

## Score
- **Score:** 4/10 — one page (/about.html) is cleanly extractable; no Organization schema, broken homepage JSON-LD, no quotable pricing.

## Limits on this read
- **Personas:** n/a — this lens reads the crawl, not persona sessions; `persona_mode` is generic, so personas elsewhere are ⚠ INFERRED
- **Not reached:** /app/login.html (robots.txt disallow), two off-domain assets; /features.html returned 404
- **Excluded:** none in manifest; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`
- **Out of scope:** live answer-engine queries; any citation claim

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — no personas in this lens, so a flip could not be observed.

## Next action
Add an Organization JSON-LD block (name, url, logo, sameAs) to every page template and repair the homepage block.
