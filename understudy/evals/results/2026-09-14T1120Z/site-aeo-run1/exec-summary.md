# Nimbus Notes — aeo — Run 2026-09-08 (fixture01)

An answer engine crawling this site today can find a valid FAQ block and a founder's name in prose, but it cannot confirm who Nimbus Notes is as an entity, and four of five crawled pages hand it nothing extractable at all.

> **Scope: static markup only.** This report judges whether an answer engine
> *could* extract and attribute this site. It does **not** query live answer
> engines and says nothing about whether the site is cited today — that half is
> not in v1.

## Coverage
| | |
|---|---|
| Pages with any structured data | 2 of 5 |
| Organization schema | absent |
| Extractable answer blocks | 3 across 1 page |
| llms.txt | absent |

## Top 3
1. **[P1] No Organization schema anywhere on the site** — machines have nothing to anchor "Nimbus Notes" to a legal entity, url, logo or sameAs. (n/a)
2. **[P2] Homepage's only structured data block is invalid JSON-LD** — the entity's primary page yields zero usable schema; crawl recorded a parse error. (n/a)
3. **[P2] Homepage has zero extractable answer blocks** — no question-shaped headings; three testimonials are the only claims, all unattributed. (n/a)

## Score
- **Score:** 4/10 — one valid (partial) FAQ block on one page is all this site offers an answer engine; the entity itself is undefined and the homepage is unreadable to schema parsers.

## Limits on this read
- **Personas:** n/a — this is a no-persona lens; `persona_mode` is `generic` per manifest, noted per policy.
- **Not reached:** `/app/login.html` (robots.txt disallow), two off-domain assets (analytics script, font CDN) — none of these carry entity or answer content.
- **Excluded:** none declared in `scope_exclusions`.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`.

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a | n/a | n/a | n/a | n/a |

## Severity flips
None — this lens has no personas, so a flip cannot be observed.

## Next action
Add `Organization` schema (name, url, logo, sameAs) site-wide and fix the truncated `price` value breaking the homepage's JSON-LD.
