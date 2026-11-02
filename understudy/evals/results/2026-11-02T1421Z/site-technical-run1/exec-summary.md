# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The home page is held back by one 3.9 MB hero PNG that pushes mobile LCP to 5.8 s in the lab, while the pricing page is fast (1.4 s mobile).

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Core Web Vitals — measured separately, reported separately
| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| / | mobile 390×844 | 5.8 s ✗ poor | 0.04 ✓ | 410 ms ⚠ | 2.9 s ⚠ | 120 ms ✓ |
| / | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 0.9 s ✓ | 110 ms ✓ |
| /pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 0.8 s ✓ | 110 ms ✓ |
| /pricing.html | desktop 1440×900 | 0.9 s ✓ | 0.01 ✓ | 10 ms ✓ | 0.5 s ✓ | 100 ms ✓ |

- All four: viewport verified, cold cache, no throttling, 1 run each.
- TBT is a lab proxy, not INP.

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 4.10 MB | 9 | 0.10 MB / 2 domains |
| / | desktop | 4.10 MB | 9 | 0.10 MB / 2 domains |
| /pricing.html | mobile | 5.2 KB | 3 | 0 |
| /pricing.html | desktop | 5.2 KB | 3 | 0 |

## Top 3
1. **[P1] Hero PNG ships 3000×2000 at 3.9 MB for a 350×233 slot, driving a 5.8 s mobile LCP** — 95% of page weight; phones pay for it first (n/a)
2. **[P2] Third-party font stylesheet blocks first paint on the home page** — mobile FCP 2.9 s; 101 KB of third-party code (n/a)
3. **[P2] Mobile TBT of 410 ms on the home page sits in needs-improvement** — phone ignores input for 410 ms (n/a)

## Score
- **Score:** 6/10 — Pricing is fast, but the home page's 3.9 MB hero gives a poor 5.8 s mobile LCP in the lab.

## Limits on this read
- **Personas:** n/a — no-persona lens; run persona_mode generic — ⚠ INFERRED
- **Not reached:** pages other than / and /pricing.html
- **Excluded:** none; auth wall never reported
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`
- **Conditions:** lab, unthrottled, single run; HTTPS/HSTS flags conflict with the http:// base URL, so unverified.

## Severity flips
- Mobile versus desktop on the home page: LCP 5.8 s poor versus 2.1 s good. Both are reported, none averaged.

## Next action
- Replace `hero.png` with a responsive AVIF/WebP under 150 KB and re-measure mobile.
