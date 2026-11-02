# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Core Web Vitals thresholds + delivery and hygiene checklist (technical-metrics.md)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (no persona applies to this lens)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Conditions: all four measurements `viewport_verified: true`, cache cold, throttling none, runs 1
- Lab numbers, one run each; none describe real users

---

## Findings

### e4939fb585a4 — Hero PNG ships 3000×2000 at 3.9 MB for a 350×233 slot, driving a 5.8 s mobile LCP
- **Severity:** P1
- **So what:** A phone downloads 3.9 MB to paint a 350×233 image; mobile LCP is 5.8 s (poor, >4.0 s) on the main landing page.
- **Framework tags:** Tier 2 image hygiene, Tier 1 LCP
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - `hero.png`: PNG, 3,900,000 B, delivered 3000×2000, displayed 350×233 mobile and 600×400 desktop, not lazy.
  - It is 95% of the 4,104,000 B page weight; mobile LCP 5.8 s, desktop 2.1 s (lab, unthrottled).
  - Delivered pixels are ~57× the mobile slot area (6.0 MP vs 0.08 MP).
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load http://localhost:8765/ at 390×844, cold cache.
  2. Read `tier2.images` and `tier1.lcp_ms`.
- **Fix:** Re-export hero as AVIF/WebP at 700px wide (1200px for desktop) via `srcset`/`sizes`, target under 150 KB.

### 0c13941671ab — Text resources are served uncompressed on both pages
- **Severity:** P2
- **So what:** HTML and CSS travel at full size on every visit, slowing first paint, most visibly on slow mobile links.
- **Framework tags:** Tier 2 compression
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - `/style.css` and `/` lack gzip/br on the home page (mobile and desktop).
  - `/style.css` and `/pricing.html` lack it on pricing (mobile and desktop).
  - style.css is 3,174 B, so the absolute saving is small; the rule is the fix.
- **Evidence:** `measure/index-mobile.json` · `measure/pricing-mobile.json` · `measure/pricing-desktop.json`
- **Repro:**
  1. Request `/style.css` and `/pricing.html` with `Accept-Encoding: br, gzip`.
  2. Check for a missing `content-encoding`.
- **Fix:** Enable brotli/gzip for text/html, text/css and JS at the server or CDN.

### 9f5725a81516 — Static assets carry no cache-control header
- **Severity:** P2
- **So what:** Returning visitors re-download the 3.9 MB hero and the stylesheet every time.
- **Framework tags:** Tier 2 cache headers
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - Home page: `hero.png` and `style.css` have no cache headers.
  - Pricing page: `style.css` has none.
  - Cold-cache lab runs only; repeat-visit cost was not measured.
- **Evidence:** `measure/index-mobile.json` · `measure/pricing-mobile.json`
- **Repro:**
  1. Request `/assets/generated/hero.png` and `/style.css`.
  2. Check for `cache-control`.
- **Fix:** Send `cache-control: public, max-age=31536000, immutable` on fingerprinted assets.

### 82d4c1e8a45a — Third-party font stylesheet blocks first paint on the home page
- **Severity:** P2
- **So what:** First paint waits on another domain's CSS; mobile FCP is 2.9 s, close to the 3.0 s poor line.
- **Framework tags:** Tier 2 render-blocking, third-party weight
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - `all.css` (62,464 B) and `style.css` both render-blocking; mobile FCP 2.9 s, desktop 0.9 s.
  - Third-party total 101,376 B over 3 requests, 2 domains: fonts 62,464 B, analytics `t.js` 38,912 B.
  - First-party is about 4.0 MB, nearly all the hero image.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
- **Repro:**
  1. Load the home page at 390×844.
  2. Read `tier2.render_blocking` and `tier2.third_party`.
- **Fix:** Subset the font, self-host with `font-display: swap`, and load `t.js` with `async`/`defer`.

### a8656f9705f1 — Mobile TBT of 410 ms on the home page sits in needs-improvement
- **Severity:** P2
- **So what:** The phone page ignores input for 410 ms after first paint, against 90 ms on desktop.
- **Framework tags:** Tier 1 TBT (a lab proxy; not INP)
- **Flow:** measure:index:mobile
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - Mobile TBT 410 ms (needs-improvement, 200–600 ms); desktop 90 ms.
  - Cause not identifiable: no JavaScript profile was taken.
  - Single run; the unthrottled machine likely understates a real phone.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
- **Repro:**
  1. Load the home page at 390×844, cold cache.
  2. Read `tier1.tbt_ms`.
- **Fix:** Profile long tasks on the home page and defer the analytics tag and any bootstrap code.

### 29c9c44e88a4 — Home page throws a ReferenceError on load
- **Severity:** P3
- **So what:** A script references a function that is not defined, so some page behaviour probably never runs.
- **Framework tags:** Tier 3 console errors on load
- **Flow:** measure:index:mobile
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - Both viewports log "ReferenceError: nimbusBootstrap is not defined" before load.
  - Pricing logs no errors.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
  > "ReferenceError: nimbusBootstrap is not defined"
- **Repro:**
  1. Open the home page with the console open.
- **Fix:** Define `nimbusBootstrap` before it is called, or remove the call.

---

## Dropped for want of evidence
- None.

## For other lenses
- The `nimbusBootstrap` ReferenceError may break page behaviour — bugs.

## Coverage gaps
- Only the home page and /pricing.html were measured; one run per viewport; no throttling; cold cache only.
- Manifest `base_url` is http://localhost:8765/ yet the measurements record `https: true` and `hsts: true`. The mismatch was not verified, so Tier 3 HTTPS/HSTS passes are untrusted.
- No field data (CrUX/RUM) exists; nothing here describes real users.

## Appendices
- C. Screenshot index: `measure/screenshots/index-mobile.png`, `index-desktop.png`, `pricing-mobile.png`, `pricing-desktop.png`
