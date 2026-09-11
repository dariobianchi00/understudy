# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The homepage ships a 3.9 MB unoptimized hero image that pushes mobile LCP to a poor 5.8 s and page weight to 4.1 MB, while the pricing page loads clean and fast on both viewports.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Top 3
1. **[P1] Unoptimized 3.9MB hero image drives page weight to 4.1MB and mobile LCP to 5.8s** — homepage hero image is 73x larger than it needs to be for its display size (n/a)
2. **[P2] Render-blocking font CSS and stylesheet delay mobile FCP on the homepage** — mobile first paint lands at 2.9s, in the "needs improvement" band (n/a)
3. **[P2] Static assets served without compression or cache headers** — style.css and the HTML document ship uncompressed; hero.png and style.css have no cache-control (n/a)

## Score
- **Score:** 6/10 — the homepage's hero image is the whole problem; fix that one asset and most of this report closes.

## Limits on this read
- **Personas:** n/a — this lens measures pages, not personas
- **Not reached:** `/features.html`, `/about.html`, `/privacy.html` — discovered by crawl, not measured (see Coverage gaps)
- **Excluded:** none
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`

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
| / | mobile | 4.10 MB | 9 | 101 KB / 2 domains |
| / | desktop | 4.10 MB | 9 | 101 KB / 2 domains |
| /pricing.html | mobile | 5.2 KB | 3 | 0 KB / 0 domains |
| /pricing.html | desktop | 5.2 KB | 3 | 0 KB / 0 domains |

## Severity flips
- n/a — no personas ran on this lens
- Worth flagging anyway: homepage LCP is "poor" on mobile (5.8 s) and "good" on desktop (2.1 s) from the *same* 4.1 MB payload — the mobile number is the real one for a marketing homepage.

## Next action
Resize and re-encode `hero.png` to its displayed dimensions (≈600×400 max) before touching anything else on this list.
