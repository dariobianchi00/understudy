# Nimbus Notes — technical — Run 2026-09-08 (fixture01)

The homepage's 3.9 MB hero image, delivered at 3000×2000px and shown at a few hundred pixels, pushes mobile LCP to 5.8s ("poor") and total page weight past 4 MB, while the pricing page loads clean and fast on both viewports.

> **Lab measurements.** One machine, one connection, one moment, cold cache.
> These identify what is wrong with the *page* — an oversized image is a fact at
> any sample size. They do **not** describe what your users experience, which
> needs field data this tool cannot reach.

## Top 3
1. **[P1] Oversized hero image drives 4.1MB page weight and 5.8s mobile LCP** — mobile visitors wait 3.7s longer than desktop for the same paint (n/a)
2. **[P2] Render-blocking stylesheets delay mobile first paint to 2.9s** — homepage FCP is "needs improvement" on mobile, "good" on desktop, same resources (n/a)
3. **[P2] Static assets ship uncompressed and without cache-control headers** — every visit re-downloads style.css and the hero image in full (n/a)

## Score
- **Score:** 6/10 — desktop is fast and clean; mobile pays a real, fixable tax for one unresized image plus missing HTTP hygiene.

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

## Limits on this read
- **Personas:** n/a — no-persona lens; measurements only, no simulated visitors.
- **Not reached:** /features.html, /about.html, /privacy.html — not in `measure/` scope, only `/` and `/pricing.html` were Tier1-3 measured.
- **Excluded:** none — `scope_exclusions` is empty in manifest.json.
- **Models:** traversal `fixture-hand-authored` · scoring `sonnet`.

## Severity flips
No personas ran under this lens — a flip cannot be observed.

## Next action
Resize/compress the hero image to its displayed dimensions (~600×400) before touching anything else on the homepage.
