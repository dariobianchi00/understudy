# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: technical-metrics.md Tier 1 (Core Web Vitals) → Tier 2 (delivery) → Tier 3 (hygiene)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens; measurements only
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Conditions: all four measurements `viewport_verified: true`, `cache: cold`, `throttling: none`, `runs: 1` — single-run lab numbers, not field data

---

## Findings

### 98fd630e58d0 — Unoptimized hero image drives poor mobile LCP and 4.1 MB page weight
- **Severity:** P1
- **So what:** Mobile visitors wait 5.8 s to see the hero — more than double the "good" LCP threshold — because the browser downloads a 3.9 MB image before it can paint.
- **Framework tags:** Tier 1 (LCP), Tier 2 (image hygiene, page weight)
- **Flow:** measure:index:mobile
- **Locator:** http://localhost:8765/assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - `hero.png` delivered at 3000×2000 natural size, 3.9 MB, PNG format, not lazy-loaded.
  - Displayed at 600×400 on desktop and 350×233 on mobile — roughly 25x more pixels than shown on mobile.
  - It is the largest asset on the page and the only image; index page total weight is 4.10 MB, of which this one file is 95%.
- **Evidence:** `measure/index-mobile.json` (tier1.lcp_ms: 5800, tier2.images[0]) · `measure/index-desktop.json` (tier1.lcp_ms: 2100, tier2.page_weight_bytes: 4104000) · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load `http://localhost:8765/` at 390×844 with a cold cache.
  2. Observe LCP fires at 5.8 s, driven by `hero.png`.
  3. Compare `naturalWidth/Height` (3000×2000) to `clientWidth/Height` (350×233 on this viewport).
- **Fix:** Re-encode `hero.png` to the largest displayed size actually needed (≈600×400 for desktop) and serve responsive sizes via `srcset`, in a modern format (WebP/AVIF).

### 4306495554da — Static assets served without cache-control headers
- **Severity:** P2
- **So what:** Every repeat visit re-downloads the stylesheet and, on the homepage, the 3.9 MB hero image, instead of reading them from the browser cache.
- **Framework tags:** Tier 2 (cache headers)
- **Flow:** measure:index:desktop
- **Locator:** http://localhost:8765/style.css
- **Personas hit:** n/a
- **Observed:**
  - `style.css` has no `cache-control` header on both the index page and the pricing page.
  - `hero.png` on the index page also has no `cache-control` header, so the 3.9 MB file re-downloads on every visit.
- **Evidence:** `measure/index-desktop.json` (tier2.missing_cache_headers) · `measure/index-mobile.json` (tier2.missing_cache_headers) · `measure/pricing-desktop.json` (tier2.missing_cache_headers) · `measure/pricing-mobile.json` (tier2.missing_cache_headers)
- **Repro:**
  1. Request `http://localhost:8765/style.css` and `http://localhost:8765/assets/generated/hero.png`.
  2. Inspect response headers — no `cache-control` present on either.
- **Fix:** Add long-lived `cache-control` headers (e.g. `max-age=31536000, immutable`) to static assets under `/style.css` and `/assets/`, with cache-busting filenames on deploy.

### 8845fb7e5ac7 — Text and CSS responses served without compression
- **Severity:** P2
- **So what:** HTML and CSS ship uncompressed on every page, adding avoidable transfer bytes on every request including the fast pricing page.
- **Framework tags:** Tier 2 (compression)
- **Flow:** measure:index:desktop
- **Locator:** http://localhost:8765/style.css
- **Personas hit:** n/a
- **Observed:**
  - `style.css` and the `/` HTML document are both listed as uncompressed text resources on the index page.
  - `style.css` and the `/pricing.html` HTML document are both listed as uncompressed on the pricing page.
- **Evidence:** `measure/index-desktop.json` (tier2.uncompressed_text_resources) · `measure/pricing-desktop.json` (tier2.uncompressed_text_resources)
- **Repro:**
  1. Request `http://localhost:8765/style.css` or `http://localhost:8765/`.
  2. Inspect response headers — no `content-encoding: gzip` or `br`.
- **Fix:** Enable gzip or brotli compression for text/html and text/css responses at the server or CDN layer.

### e6edd96102f6 — Render-blocking external font stylesheet delays first paint
- **Severity:** P2
- **So what:** The homepage waits on a cross-origin stylesheet before rendering anything, contributing to a 2.9 s mobile FCP.
- **Framework tags:** Tier 2 (render-blocking)
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - `fonts.example-cdn.test/all.css` and the local `style.css` are both render-blocking in `<head>` on the index page.
  - Mobile FCP is 2.9 s ("needs improvement" band) versus 900 ms on desktop for the same page.
- **Evidence:** `measure/index-mobile.json` (tier1.fcp_ms: 2900, tier2.render_blocking) · `measure/index-desktop.json` (tier2.render_blocking)
- **Repro:**
  1. Load `http://localhost:8765/` at 390×844, cold cache.
  2. Observe both stylesheets block first paint until fetched.
- **Fix:** Preconnect to `fonts.example-cdn.test`, and inline or preload critical CSS so first paint does not wait on the round trip.

### 8c5c120a71ea — Console error fires on every homepage load
- **Severity:** P3
- **So what:** A `ReferenceError` fires before `load` on every homepage visit — a hygiene signal, not scored as a functional bug by this lens.
- **Framework tags:** Tier 3 (console errors on load)
- **Flow:** measure:index:mobile
- **Locator:** http://localhost:8765/
- **Personas hit:** n/a
- **Observed:**
  - `console_errors_on_load` reports `"ReferenceError: nimbusBootstrap is not defined"` on both index-mobile and index-desktop measurements.
  - Does not appear on the pricing page.
- **Evidence:** `measure/index-mobile.json` (tier3.console_errors_on_load) · `measure/index-desktop.json` (tier3.console_errors_on_load)
- **Repro:**
  1. Load `http://localhost:8765/` with devtools console open.
  2. Observe `ReferenceError: nimbusBootstrap is not defined` before `load` fires.
- **Fix:** Ensure the script defining `nimbusBootstrap` loads and executes before the call site, or guard the call with an existence check.

---

## Dropped for want of evidence
- None — all four measurement files were complete and usable.

## For other lenses
- `ReferenceError: nimbusBootstrap is not defined` may indicate broken homepage functionality beyond a load-time hygiene signal — worth a functional check by the `bugs` lens.

## Coverage gaps
- Only two pages measured (index, pricing); no other site pages were captured under Mode B.

## Appendices
- A. Persona debriefs — n/a, no-persona lens.
- B. Session timelines — n/a, single-shot lab measurements.
- C. Screenshot index — `measure/screenshots/index-desktop.png`, `measure/screenshots/index-mobile.png`, `measure/screenshots/pricing-desktop.png`, `measure/screenshots/pricing-mobile.png`.
