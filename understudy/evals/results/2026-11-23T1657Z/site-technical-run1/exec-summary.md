# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The home page is held back on mobile by one 3.9 MB hero image (LCP 5.8 s, lab), while the pricing page is fast and light on both viewports.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Core Web Vitals — measured separately, reported separately
| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| / | mobile 390×844 | 5.8 s ⚠ poor | 0.04 ✓ | 410 ms ⚠ | 2.9 s ⚠ | 120 ms ✓ |
| / | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 0.9 s ✓ | 110 ms ✓ |
| /pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 0.8 s ✓ | 110 ms ✓ |
| /pricing.html | desktop 1440×900 | 0.9 s ✓ | 0.01 ✓ | 10 ms ✓ | 0.5 s ✓ | 100 ms ✓ |

- Each cell is one run, no throttling, cold cache, viewport verified. Nothing was measured twice.
- TBT is a lab proxy, not INP.

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 4.1 MB | 9 | 101 KB / 2 domains |
| / | desktop | 4.1 MB | 9 | 101 KB / 2 domains |
| /pricing.html | mobile | 5.2 KB | 3 | 0 |
| /pricing.html | desktop | 5.2 KB | 3 | 0 |

- Hero image is 3.9 MB of the 4.1 MB on the home page (95%).
- Third-party on `/`: 101 KB (fonts 62 KB, analytics 39 KB). The rest is first-party.

## Top 3
1. **[P1] 3.9 MB hero.png delivered at 3000×2000 and shown at 350×233 drives mobile LCP to 5.8 s** — 95% of home-page bytes; mobile LCP is in the "poor" band (n/a)
2. **[P2] HTML and style.css are served without compression on both pages** — text sent uncompressed on every load (n/a)
3. **[P2] No cache-control on style.css or hero.png, so repeat visitors re-download 3.9 MB** — every return visit may pay full weight (n/a)

## Score
- **Score:** 7/10 — Pricing is fast; the home page's mobile load is poor because of one fixable image.

## Limits on this read
- **Personas:** n/a — no-persona lens; manifest `persona_mode` is generic
- **Not reached:** pages other than `/` and `/pricing.html`; repeat visits; field data
- **Excluded:** none; auth wall never scored
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
- None across personas (no-persona lens). Viewport difference: home LCP 5.8 s mobile vs 2.1 s desktop from the same image.

## Next action
Resize hero.png to about 700 px wide, convert to WebP/AVIF, and enable compression and cache headers.
