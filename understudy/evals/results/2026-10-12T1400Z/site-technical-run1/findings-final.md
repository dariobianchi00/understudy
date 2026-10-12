# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Core Web Vitals, delivery, hygiene (technical-metrics.md); lab numbers only
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — generic mode, no persona lens
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Lab data: 1 run per page/viewport, cold cache, no throttling, localhost. Not user experience.

---

## Findings

### e203b2f35975 — 3.9 MB hero PNG delivered at 3000×2000 drives 5.8 s mobile LCP
- **Severity:** P1
- **So what:** Mobile LCP is in the "poor" band (>4.0 s) and the page weighs 4.10 MB because of one image.
- **Framework tags:** Tier 1 LCP, Tier 2 image hygiene, page weight
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - Delivered 3000×2000 PNG, 3,900,000 bytes; displayed 350×233 on mobile (~99% of pixels wasted), 600×400 on desktop.
  - Not lazy-loaded; no cache-control header. Mobile LCP 5.8 s vs desktop 2.1 s.
  - Page weight 4,104,000 bytes; hero is ~95%.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load http://localhost:8765/ cold at 390×844.
  2. Read tier1.lcp_ms (5800) and tier2.images[0].
- **Fix:** Re-export hero as WebP/AVIF at ≤800px wide (target <150 KB), add `srcset`/`sizes`, serve with long cache-control.

### 0749de42ff3f — Text responses uncompressed and static assets lack cache headers on both pages
- **Severity:** P2
- **So what:** Every first visit sends HTML/CSS at full size and repeat visits cannot reuse assets.
- **Framework tags:** Tier 2 compression, cache headers
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - No gzip/br on /style.css, / and /pricing.html (pricing page 5.2 KB total, so small absolute cost).
  - No cache-control on /style.css (both pages) and hero.png (home).
- **Evidence:** `measure/index-mobile.json` · `measure/pricing-mobile.json` · `measure/pricing-desktop.json`
- **Repro:**
  1. Inspect response headers for /style.css.
  2. Compare tier2.uncompressed_text_resources and missing_cache_headers.
- **Fix:** Enable gzip/brotli for text types and set `cache-control: public, max-age=31536000, immutable` on fingerprinted static assets.

### 82c774e70e1c — Render-blocking third-party font CSS holds mobile FCP at 2.9 s
- **Severity:** P2
- **So what:** Nothing paints until a stylesheet from another domain arrives; mobile FCP 2.9 s is just inside "needs improvement".
- **Framework tags:** Tier 1 FCP, Tier 2 render-blocking, third-party
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - Render-blocking in head: fonts.example-cdn.test/all.css (62,464 bytes) and /style.css.
  - Third-party total 101,376 bytes over 2 domains (fonts 62,464; analytics.example-tracker.test 38,912).
  - Mobile FCP 2.9 s vs desktop 0.9 s.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
- **Repro:**
  1. Load / cold at 390×844.
  2. Read tier2.render_blocking and tier1.fcp_ms.
- **Fix:** Self-host a subset of the fonts with `font-display: swap`, preload the primary file, and load analytics with `async`/`defer`.

### 2fc5d2fa5dd9 — Mobile TBT of 410 ms on the home page needs improvement
- **Severity:** P2
- **So what:** The page ignored input for 410 ms in this lab run; TBT is a proxy, not measured interaction latency.
- **Framework tags:** Tier 1 TBT
- **Flow:** measure:index:mobile
- **Locator:** tier1.tbt_ms
- **Personas hit:** n/a
- **Observed:**
  - Mobile TBT 410 ms (needs-improvement band 200–600 ms); desktop 90 ms; pricing 30 ms / 10 ms.
  - Cause not identifiable: no JavaScript profile in this capture.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
- **Repro:**
  1. Load / cold at 390×844.
  2. Read tier1.tbt_ms (410).
- **Fix:** Profile main-thread long tasks on mobile and defer or split non-critical scripts, starting with the analytics tag.

### 755122606318 — Home page throws ReferenceError on load: nimbusBootstrap is not defined
- **Severity:** P3
- **So what:** A script error on load is a hygiene signal that something expected to initialise did not.
- **Framework tags:** Tier 3 console errors on load
- **Flow:** measure:index:mobile
- **Locator:** nimbusBootstrap
- **Personas hit:** n/a
- **Observed:**
  - Same error at 390×844 and 1440×900; none on /pricing.html.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
  > "ReferenceError: nimbusBootstrap is not defined"
- **Repro:**
  1. Load / and read tier3.console_errors_on_load.
- **Fix:** Define or load `nimbusBootstrap` before it is called, or remove the call.

---

## Dropped for want of evidence
- None.

## For other lenses
- Console error may break page behaviour — bugs.

## Coverage gaps
- Only / and /pricing.html measured; single run each; no throttling, no field data, no repeat visits.
- Tier 3: HTTPS, HSTS, viewport meta pass; no mixed content, redirects or 404s.

## Appendices
- A. n/a
- B. n/a
- C. `measure/screenshots/`
