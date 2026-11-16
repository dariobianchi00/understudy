# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The home page ships a 3.9 MB hero PNG that puts mobile LCP at 5.8 s (poor), while the pricing page is fast and light at 1.4 s on mobile.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Core Web Vitals — measured separately, reported separately
| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| / | mobile 390×844 | 5.8 s ⚠ | 0.04 ✓ | 410 ms ⚠ | 2.9 s ⚠ | 120 ms ✓ |
| / | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 0.9 s ✓ | 110 ms ✓ |
| /pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 0.8 s ✓ | 110 ms ✓ |
| /pricing.html | desktop 1440×900 | 0.9 s ✓ | 0.01 ✓ | 10 ms ✓ | 0.5 s ✓ | 100 ms ✓ |

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 4.1 MB | 9 | 99 KB / 2 domains |
| / | desktop | 4.1 MB | 9 | 99 KB / 2 domains |
| /pricing.html | mobile | 5.2 KB | 3 | 0 |
| /pricing.html | desktop | 5.2 KB | 3 | 0 |

## Top 3
1. **[P1] Hero PNG is 3.9 MB, delivered at 3000×2000 and shown at 350×233** — 95% of page weight; mobile LCP 5.8 s poor (n/a)
2. **[P2] HTML and style.css uncompressed, no cache-control** — every visit re-pays full cost (n/a)
3. **[P2] Third-party fonts CSS blocks render** — mobile FCP 2.9 s, 0.1 s from poor (n/a)

## Score
- **Score:** 6/10 — Pricing is fast; the home page's one oversized image makes mobile LCP poor, an easy fix.

## Limits on this read
- **Personas:** n/a — no-persona lens; `persona_mode` generic, ⚠ INFERRED where personas are used elsewhere
- **Not reached:** other pages; repeat visits; throttled networks; field data
- **Excluded:** none; auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`
- Single run per measurement (`runs: 1`), so variance is unknown.

## Severity flips
- Mobile vs desktop on `/`: LCP 5.8 s vs 2.1 s — same image, so the desktop figure flatters it.

## Next action
- Re-export hero.png at ≤700 px as WebP/AVIF and re-measure mobile.
