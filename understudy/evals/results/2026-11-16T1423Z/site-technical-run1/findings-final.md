# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Core Web Vitals (Tier 1) explained by delivery (Tier 2), then hygiene checklist (Tier 3)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (no persona lens here; measurements only)
- Scoring model: sonnet
- **Lab measurements:** one run, one machine, cold cache, no throttling, 2026-09-08 09:30 UTC. They describe the page, not your users.
- All four measurements have `viewport_verified: true`, `runs: 1` — no variance observed, none testable.
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### afc5c524a940 — Hero PNG is 3.9 MB, delivered at 3000×2000 and shown at 350×233, driving a 5.8 s mobile LCP
- **Severity:** P1
- **So what:** Mobile LCP is "poor" (5.8 s > 4.0 s) on the primary page, and the one asset is 95% of a 4.1 MB page.
- **Framework tags:** Tier 2 image hygiene, Tier 1 LCP
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - Mobile: 3000×2000 PNG, 3,900,000 B, displayed 350×233; ~98.7% of delivered pixels unused. Not lazy (above fold, correct).
  - Desktop: same file, displayed 600×400; LCP 2.1 s ✓ (flattering — no throttling).
  - Page weight 4,104,000 B, 9 requests, both viewports.
- **Evidence:** `measure/index-mobile.json` (tier2.images, tier1.lcp_ms) · `measure/index-desktop.json` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Open `/` at 390×844, cold cache.
  2. Read the largest asset and LCP from the network log.
- **Fix:** Re-export hero.png as WebP/AVIF at ≤700 px wide (≈1050 px for 2× mobile), with `srcset`; target under 150 KB.

### 39ace225e601 — HTML and style.css are served uncompressed with no cache-control on the home and pricing pages
- **Severity:** P2
- **So what:** Every first visit sends text at full size, and repeat visits cannot reuse style.css or the hero.
- **Framework tags:** Tier 2 compression, Tier 2 cache headers
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - No gzip/br on `/`, `/pricing.html` and `/style.css` (style.css is 3,174 B — small gain).
  - No `cache-control` on `/style.css` or `/assets/generated/hero.png` (3.9 MB re-downloadable every visit).
  - Same on mobile and desktop; pricing page affected too (`/pricing.html`).
- **Evidence:** `measure/index-mobile.json` (uncompressed_text_resources, missing_cache_headers) · `measure/pricing-mobile.json`
- **Repro:**
  1. Request `/style.css`; inspect `content-encoding` and `cache-control`.
- **Fix:** Enable br/gzip for text types on the server; set `Cache-Control: public, max-age=31536000, immutable` on hashed static assets.

### a9f93bd34211 — Third-party fonts stylesheet blocks render on the home page, alongside a 39 KB analytics script
- **Severity:** P2
- **So what:** Mobile FCP is 2.9 s (needs improvement, 0.1 s from poor) while the page waits on another domain's CSS.
- **Framework tags:** Tier 2 render-blocking, Tier 2 third-party
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - Render-blocking in `<head>`: fonts.example-cdn.test/all.css (62,464 B) and /style.css.
  - Third-party total 101,376 B across 2 domains, 3 requests; first-party ≈ 4.0 MB.
  - analytics.example-tracker.test/t.js: 38,912 B.
- **Evidence:** `measure/index-mobile.json` (tier2.render_blocking, tier2.third_party, tier1.fcp_ms)
- **Repro:**
  1. Load `/` cold; list `<head>` stylesheets without `media`/async.
- **Fix:** Self-host the needed font subset with `font-display: swap` and `preload`; load t.js with `async`/`defer`.

### e9ff32265a2b — Mobile TBT of 410 ms on the home page is in the needs-improvement band, cause not isolated
- **Severity:** P2
- **So what:** The page ignores input for 410 ms on mobile (desktop 90 ms ✓); this is a lab proxy, not INP.
- **Framework tags:** Tier 1 TBT
- **Flow:** measure:index:mobile
- **Locator:** tbt_ms
- **Personas hit:** n/a
- **Observed:**
  - Mobile TBT 410 ms (≤200 good, ≤600 needs work); desktop 90 ms.
  - Measurement has no JS profiling; the failing `nimbusBootstrap` script and the analytics tag are candidates, unproven.
- **Evidence:** `measure/index-mobile.json` (tier1.tbt_ms) · `measure/index-desktop.json`
- **Repro:**
  1. Record a performance trace of `/` at 390×844; list long tasks after FCP.
- **Fix:** Profile long tasks on mobile and defer or split the biggest scripts; re-measure.

### 92464b3b93ee — Home page throws a ReferenceError for nimbusBootstrap on load
- **Severity:** P3
- **So what:** A script error before `load` signals broken or dead code, and may add main-thread cost.
- **Framework tags:** Tier 3 console errors on load
- **Flow:** measure:index:desktop
- **Locator:** nimbusBootstrap
- **Personas hit:** n/a
- **Observed:**
  - `ReferenceError: nimbusBootstrap is not defined` on both viewports.
  - Impact on behaviour not assessed here (bugs lens).
- **Evidence:** `measure/index-desktop.json` (tier3.console_errors_on_load) · `measure/index-mobile.json`
- **Repro:**
  1. Open `/` and read the console before `load`.
- **Fix:** Define `nimbusBootstrap` before it is called, or delete the call if the script no longer ships.

---

## Dropped for want of evidence
- None.

## For other lenses
- Console error `nimbusBootstrap is not defined` may break page behaviour — bugs.

## Coverage gaps
- Only `/` and `/pricing.html` measured; one run each, no throttling, no warm-cache or field data.
- HSTS reported true over `http://localhost`; not independently verified.

## Appendices
- C. Screenshot index: `measure/screenshots/{index,pricing}-{mobile,desktop}.png`
