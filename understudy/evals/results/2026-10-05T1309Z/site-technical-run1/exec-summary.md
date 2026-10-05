# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The landing page is slowed by one 3.9 MB PNG hero that pushes mobile LCP to 5.8 s (poor), while the pricing page is fast and light on both viewports.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Core Web Vitals — measured separately, reported separately
- Conditions: `viewport_verified` true on all four; cold cache; no throttling; 1 run each; 2026-09-08.

| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| / | mobile 390×844 | 5.8 s ✗ poor | 0.04 ✓ | 410 ms ⚠ | 2.9 s ⚠ | 120 ms ✓ |
| / | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 0.9 s ✓ | 110 ms ✓ |
| /pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 0.8 s ✓ | 110 ms ✓ |
| /pricing.html | desktop 1440×900 | 0.9 s ✓ | 0.01 ✓ | 10 ms ✓ | 0.5 s ✓ | 100 ms ✓ |

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 4.10 MB | 9 | 101 KB / 2 domains |
| / | desktop | 4.10 MB | 9 | 101 KB / 2 domains |
| /pricing.html | mobile | 5.2 KB | 3 | 0 |
| /pricing.html | desktop | 5.2 KB | 3 | 0 |

- First-party: 4.00 MB of the landing page, 3.9 MB of it one image.

## Top 3
1. **[P1] 3.9 MB 3000×2000 PNG hero shown at 350×233 drives 5.8 s mobile LCP** — 95% of page weight; fixing the image helps LCP, weight and FCP (n/a)
2. **[P2] Mobile TBT of 410 ms on the landing page sits in needs-improvement** — page ignored input for 410 ms; TBT is a lab proxy, not INP (n/a)
3. **[P2] Third-party font stylesheet blocks render, FCP 2.9 s on mobile** — nothing paints until an external CSS file arrives (n/a)

## Score
- **Score:** 7/10 — pricing page is fast and light; the landing page's one 3.9 MB image is the single large, easily fixed cost.

## Limits on this read
- **Personas:** n/a — no-persona lens; measurements only
- **Not reached:** /features, /about, /privacy were not measured
- **Excluded:** none; auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`
- Lab numbers; one run per page; desktop figures flatter the page.

## Numbers
- 4 measurements, all with verified viewport; none discarded.

## Severity flips
- None — no personas; mobile and desktop differ on the same causes (hero LCP poor on mobile, good on desktop).

## Next action
- Re-export the hero as ~700 px wide WebP/AVIF (<100 KB) and re-measure mobile.
