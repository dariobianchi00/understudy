# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Core Web Vitals + delivery/hygiene checks from `technical-metrics.md`, mobile and desktop scored separately
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens; `persona_mode: generic` in manifest applies to other lenses, not this one
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### dd34a0204312 — Unresized hero image drives mobile LCP to 5.8 s
- **Severity:** P1
- **So what:** Mobile visitors to the homepage — the primary marketing page — wait 5.8 s to see the largest content, past Google's 4.0 s "poor" line.
- **Framework tags:** Tier 1 (LCP), Tier 2 (image hygiene, page weight)
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - Homepage mobile: LCP 5,800 ms (poor, threshold 4,000 ms); desktop: LCP 2,100 ms (good) — same asset, viewport-dependent outcome.
  - `hero.png` delivered at 3000×2000 natural resolution, 3,900,000 bytes; displayed at 350×233 (mobile) / 600×400 (desktop).
  - Hero image is 3.9 MB of the homepage's 4.1 MB total weight (95%) — the single largest asset on the page by a wide margin.
- **Evidence:** `measure/index-mobile.json` (tier1.lcp_ms, tier2.images[0]) · `measure/index-desktop.json` (tier1.lcp_ms, tier2.images[0]) · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load `http://localhost:8765/` on a cold cache at 390×844.
  2. Observe LCP candidate is the hero image, painted at 5.8 s.
  3. Compare `tier2.images[0].natural` (3000×2000) to `.displayed` (350×233) in `measure/index-mobile.json`.
- **Fix:** Serve `hero.png` resized/re-encoded to match its largest displayed size (~600×400 desktop) with responsive `srcset`, targeting well under 200 KB.

### 832af2d0b5b1 — Render-blocking stylesheet and font CSS delay first paint
- **Severity:** P2
- **So what:** Two render-blocking resources in `<head>` push back first paint on every page load, on every page.
- **Framework tags:** Tier 2 (render-blocking)
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - Homepage: `style.css` (first-party) and `https://fonts.example-cdn.test/all.css` (third-party, 62,464 bytes) both block render.
  - Pricing page: `style.css` alone blocks render; no font CSS present there.
  - Homepage mobile FCP is 2.9 s (needs improvement, threshold 1.8 s good); pricing mobile FCP is 0.8 s on a page with no blocking third party.
- **Evidence:** `measure/index-mobile.json` (tier2.render_blocking) · `measure/pricing-mobile.json` (tier2.render_blocking)
- **Repro:**
  1. Load `http://localhost:8765/` cold.
  2. Inspect `tier2.render_blocking` in `measure/index-mobile.json` — lists both stylesheets.
- **Fix:** Inline critical CSS for above-the-fold content; load `all.css` and the rest of `style.css` with `media="print" onload` swap or `<link rel=preload>`.

### 4748085f3df5 — CSS and HTML served without compression
- **Severity:** P2
- **So what:** Every visitor downloads uncompressed text on every page, adding avoidable transfer time with no upside.
- **Framework tags:** Tier 2 (compression)
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - Homepage: `style.css` and the `/` document itself have no `content-encoding` (gzip/br).
  - Pricing page: `style.css` and `/pricing.html` are also uncompressed.
  - Same `style.css` file is served uncompressed on both pages measured.
- **Evidence:** `measure/index-mobile.json` (tier2.uncompressed_text_resources) · `measure/pricing-mobile.json` (tier2.uncompressed_text_resources)
- **Repro:**
  1. Request `http://localhost:8765/style.css` and inspect response headers.
  2. No `content-encoding` present; compare against `tier2.uncompressed_text_resources` in either measure file.
- **Fix:** Enable gzip or brotli compression for text responses (HTML, CSS, JS) at the server or CDN.

### 291ae6766813 — Static assets served without cache-control headers
- **Severity:** P2
- **So what:** Repeat visits to any page re-download the same unchanged CSS and hero image instead of using a local cache.
- **Framework tags:** Tier 2 (cache headers)
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - Homepage: `style.css` and `hero.png` both have no (or trivially short) `cache-control`.
  - Pricing page: `style.css` also has no `cache-control`.
  - This run measured cold cache only, so no repeat-visit timing was captured — the header absence itself is the fact reported here.
- **Evidence:** `measure/index-mobile.json` (tier2.missing_cache_headers) · `measure/pricing-mobile.json` (tier2.missing_cache_headers)
- **Repro:**
  1. Request `http://localhost:8765/style.css` and `http://localhost:8765/assets/generated/hero.png`.
  2. Inspect `cache-control` response header; compare to `tier2.missing_cache_headers` in the measure files.
- **Fix:** Add long `max-age` `cache-control` headers (with content-hashed filenames) to static CSS and image assets.

### ba1f15104084 — Uncaught ReferenceError fires before homepage load completes
- **Severity:** P3
- **So what:** A broken script reference is a hygiene signal on an otherwise-clean page; no measured effect on load metrics.
- **Framework tags:** Tier 3 (console errors on load)
- **Flow:** measure:index:mobile
- **Locator:** console:nimbusBootstrap
- **Personas hit:** n/a
- **Observed:**
  - `ReferenceError: nimbusBootstrap is not defined` recorded before `load` fires, on both homepage mobile and desktop measurements.
  - Pricing page has zero console errors on load.
  - CLS (0.04/0.02) and TBT (410/90 ms) show no measurable disruption from the error.
- **Evidence:** `measure/index-mobile.json` (tier3.console_errors_on_load) · `measure/index-desktop.json` (tier3.console_errors_on_load)
- **Repro:**
  1. Load `http://localhost:8765/` with devtools console open.
  2. Observe `ReferenceError: nimbusBootstrap is not defined` before the load event.
- **Fix:** Define or remove the `nimbusBootstrap` reference so the homepage loads without a console error.

---

## Dropped for want of evidence
- Third-party weight (99 KB / 2 domains on the homepage) — not pursued as a standalone finding; too small relative to the hero image to be the site's third-party weight story. Not dropped for missing evidence, just folded into Finding 832af2d0b5b1's observed bullets.

## For other lenses
- `ReferenceError: nimbusBootstrap is not defined` may indicate a broken feature — functional impact, if any, belongs to the `bugs` lens.

## Coverage gaps
- Only `/` and `/pricing.html` were measured this run; no other pages (signup, docs, etc.) have technical measurements.
- No throttled-network measurement was taken — all numbers are un-throttled lab conditions per `tier1`/`throttling: none`.
- No repeat-visit / warm-cache measurement — cold cache only, so cache-header impact is reported as a fact, not a timing.

## Appendices
- A. Persona debriefs — n/a, no-persona lens
- B. Session timelines — n/a, no-persona lens
- C. Screenshot index — `measure/screenshots/index-mobile.png`, `measure/screenshots/index-desktop.png`, `measure/screenshots/pricing-mobile.png`, `measure/screenshots/pricing-desktop.png`
