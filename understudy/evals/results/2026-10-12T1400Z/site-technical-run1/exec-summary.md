# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The home page is held back by one 3.9 MB hero PNG that pushes mobile LCP to 5.8 s in this lab run, while pricing is fast on both viewports.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

- Conditions: `viewport_verified` true on all four; cache cold; throttling none; runs 1 each — no variance observed.

## Core Web Vitals — measured separately, reported separately
| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| / | mobile 390×844 | 5.8 s ✗ | 0.04 ✓ | 410 ms ⚠ | 2.9 s ⚠ | 120 ms ✓ |
| / | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 0.9 s ✓ | 110 ms ✓ |
| /pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 0.8 s ✓ | 110 ms ✓ |
| /pricing.html | desktop 1440×900 | 0.9 s ✓ | 0.01 ✓ | 10 ms ✓ | 0.5 s ✓ | 100 ms ✓ |

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 4.10 MB | 9 | 99 KB / 2 domains |
| / | desktop | 4.10 MB | 9 | 99 KB / 2 domains |
| /pricing.html | mobile | 5.2 KB | 3 | 0 |
| /pricing.html | desktop | 5.2 KB | 3 | 0 |

- First-party: hero PNG is 3.9 MB of the 4.10 MB home page; third-party is 101,376 bytes, not the problem.

## Top 3
1. **[P1] 3.9 MB hero PNG delivered at 3000×2000 drives 5.8 s mobile LCP** — shown at 350×233 on mobile; ~95% of the page's bytes (n/a)
2. **[P2] Render-blocking third-party font CSS holds mobile FCP at 2.9 s** — nothing paints until a third-party stylesheet returns (n/a)
3. **[P2] Mobile TBT of 410 ms on the home page needs improvement** — page ignores input for 410 ms in this lab run (n/a)

## Score
- **Score:** 6/10 — pricing is fast everywhere; the home page's mobile load is poor from one fixable image.

## Limits on this read
- **Personas:** n/a — no-persona lens; manifest `persona_mode` is generic
- **Not reached:** pages other than / and /pricing.html; repeat visits; field data
- **Excluded:** none; auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Severity flips
None — no persona lens; mobile and desktop differ in degree (LCP 5.8 s vs 2.1 s) and are reported separately.

## Next action
Convert the hero to a ~700px-wide WebP/AVIF with `srcset`, then re-measure mobile.
