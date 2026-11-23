# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Core Web Vitals thresholds (Tier 1), delivery (Tier 2), hygiene (Tier 3) from `technical-metrics.md`
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a (no-persona lens); manifest `persona_mode` is generic
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

> **Lab measurements.** One machine, one connection, one moment, cold cache, no throttling, one run each.
> These describe the *page*, not what users experience; that needs field data this tool cannot reach.
> All four measurements had `viewport_verified: true`.

---

## Findings

### 72fb2e2f358e — 3.9 MB hero.png delivered at 3000×2000 and shown at 350×233 drives mobile LCP to 5.8 s
- **Severity:** P1
- **So what:** One image is 95% of the home page's 4.1 MB and puts mobile LCP in the poor band.
- **Framework tags:** Tier 2 image hygiene, Tier 1 LCP
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - Delivered 3000×2000 PNG, 3,900,000 bytes, not lazy; displayed 350×233 mobile, 600×400 desktop.
  - Mobile LCP 5.8 s (poor, >4.0 s); desktop LCP 2.1 s (good). Page weight 4,104,000 bytes.
  - Mobile: 6.0 MP delivered vs 0.08 MP displayed, about 99% of pixels unused.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load `/` at 390×844, cold cache, no throttling.
  2. Read LCP and the image entry in the resource log.
- **Fix:** Export hero.png at about 700 px wide as WebP/AVIF with srcset; target under 150 KB.

### 680519eda4f3 — HTML and style.css are served without compression on both pages
- **Severity:** P2
- **So what:** Text resources ship at full size on every first visit.
- **Framework tags:** Tier 2 compression
- **Flow:** measure:index:mobile
- **Locator:** /style.css
- **Personas hit:** n/a
- **Observed:**
  - Uncompressed on `/`: `/style.css`, `/`. Also on `/pricing.html`: `/style.css`, `/pricing.html`.
  - style.css is 3,174 bytes; the saving is small in absolute terms.
- **Evidence:** `measure/index-mobile.json` · `measure/pricing-mobile.json`
- **Repro:**
  1. Request `/style.css` and `/`; check `content-encoding`.
- **Fix:** Enable gzip or brotli for text/html and text/css on the server.

### 1d65e4dc2aca — No cache-control on style.css or hero.png, so repeat visitors re-download 3.9 MB
- **Severity:** P2
- **So what:** Every return visit may re-fetch the 3.9 MB image.
- **Framework tags:** Tier 2 cache headers
- **Flow:** measure:index:mobile
- **Locator:** /assets/generated/hero.png#cache
- **Personas hit:** n/a
- **Observed:**
  - Missing on `/style.css` and `/assets/generated/hero.png` (home); `/style.css` on pricing.
  - Repeat visits were not measured; consequence is inferred from the headers only.
- **Evidence:** `measure/index-mobile.json` · `measure/pricing-mobile.json`
- **Repro:**
  1. Request each asset; check for `cache-control`.
- **Fix:** Add `Cache-Control: public, max-age=31536000, immutable` to fingerprinted assets.

### 581020e133bc — Render-blocking third-party font stylesheet holds mobile FCP at 2.9 s
- **Severity:** P2
- **So what:** Nothing paints until a 62 KB stylesheet from another domain arrives; mobile FCP is 2.9 s, near the poor line.
- **Framework tags:** Tier 2 render-blocking, Tier 2 third-party, Tier 1 FCP, TBT
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - Render-blocking in `<head>`: `fonts.example-cdn.test/all.css` (62,464 B) and `/style.css`.
  - Mobile FCP 2.9 s (needs improvement), TBT 410 ms (needs improvement); desktop FCP 0.9 s, TBT 90 ms.
  - Third-party total 101,376 B, 2 domains, 3 requests (fonts 62,464 B, analytics 38,912 B).
- **Evidence:** `measure/index-mobile.json`
- **Repro:**
  1. Load `/` at 390×844; list render-blocking resources.
- **Fix:** Subset fonts, self-host them with `font-display: swap`, and defer the analytics script.

### 755122606318 — Home page throws ReferenceError on load: nimbusBootstrap is not defined
- **Severity:** P3
- **So what:** A script failing on load is a hygiene signal and may leave something unfinished.
- **Framework tags:** Tier 3 console errors on load
- **Flow:** measure:index:mobile
- **Locator:** nimbusBootstrap
- **Personas hit:** n/a
- **Observed:**
  - Error present on `/` at both viewports; none on `/pricing.html`.
- **Evidence:** `measure/index-mobile.json` · `measure/index-desktop.json`
  > "ReferenceError: nimbusBootstrap is not defined"
- **Repro:**
  1. Open `/` with the console open and read errors before `load`.
- **Fix:** Define or load `nimbusBootstrap` before it is called, or remove the call.

---

## Dropped for want of evidence
- None.

## For other lenses
- Console error may indicate broken on-page behaviour — bugs lens.

## Coverage gaps
- Only `/` and `/pricing.html` measured; single run each; no repeat-visit or field data.
- Tier 3 passed on both pages: HTTPS, HSTS, viewport meta, no redirects, no 404s, no mixed content.

## Appendices
- C. Screenshot index: `measure/screenshots/index-mobile.png`, `index-desktop.png`, `pricing-mobile.png`, `pricing-desktop.png`
