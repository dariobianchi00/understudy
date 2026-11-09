# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

One uncompressed 3.9 MB hero PNG makes the landing page 4.1 MB and pushes its mobile lab LCP to 5.8 s (poor), while the pricing page is fast and light.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Core Web Vitals — measured separately, reported separately
| Page | Viewport | LCP | CLS | TBT | FCP | TTFB |
|---|---|---|---|---|---|---|
| http://localhost:8765/ | mobile 390×844 | 5.8 s ✗ poor | 0.04 ✓ | 410 ms ⚠ | 2.9 s ⚠ | 120 ms ✓ |
| http://localhost:8765/ | desktop 1440×900 | 2.1 s ✓ | 0.02 ✓ | 90 ms ✓ | 0.9 s ✓ | 110 ms ✓ |
| http://localhost:8765/pricing.html | mobile 390×844 | 1.4 s ✓ | 0.01 ✓ | 30 ms ✓ | 0.8 s ✓ | 110 ms ✓ |
| http://localhost:8765/pricing.html | desktop 1440×900 | 0.9 s ✓ | 0.01 ✓ | 10 ms ✓ | 0.5 s ✓ | 100 ms ✓ |

- All four measurements: `viewport_verified: true`, cache cold, no throttling, 1 run each.
- TBT is a lab proxy, not INP; INP needs real users.

## Weight
| Page | Viewport | Weight | Requests | Third-party |
|---|---|---|---|---|
| / | mobile | 4.10 MB | 9 | 99 KB / 2 domains (3 requests) |
| / | desktop | 4.10 MB | 9 | 99 KB / 2 domains (3 requests) |
| /pricing.html | mobile | 5.2 KB | 3 | 0 |
| /pricing.html | desktop | 5.2 KB | 3 | 0 |

- First-party is ~4.0 MB of the landing page, of which hero.png is 3.9 MB.

## Top 3
1. **[P1] 3.9 MB hero PNG at 3000×2000 shown at 350×233** — ~99% of its pixels are discarded; mobile LCP 5.8 s (n/a)
2. **[P2] Text uncompressed, no cache headers** — every visit re-downloads style.css and hero.png (n/a)
3. **[P2] Third-party font CSS is render-blocking** — mobile FCP 2.9 s, near the 3.0 s poor line (n/a)

## Score
- **Score:** 6/10 — pricing page is fast and light; the landing page's mobile load is held back by one image that is easy to fix.

## Limits on this read
- **Personas:** n/a — technical lens uses measurements, not personas. `persona_mode` is generic; personas were INFERRED, and this lens does not rest on them.
- **Not reached:** features, about and privacy pages were not measured; features returned a 404 in the evaluator session (other lens).
- **Excluded:** none; auth wall never reported.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| n/a (lab measurement) | n/a | / mobile: at risk; others healthy | n/a | n/a |

## Severity flips
- None. Mobile versus desktop differ in degree (LCP 5.8 s vs 2.1 s), not in severity of cause.

## Next action
- Re-export hero.png as ~700×467 WebP/AVIF under 150 KB, then enable gzip/br and cache headers.
