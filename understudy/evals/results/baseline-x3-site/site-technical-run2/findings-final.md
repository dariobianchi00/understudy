# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: technical-metrics.md — Tier 1 Core Web Vitals, Tier 2 delivery, Tier 3 hygiene
- Pass 1 naive capture (Mode B measure) → Pass 2 analyst scoring
- Personas: n/a — this lens scores measurements, not personas
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- ⚑ All numbers below are lab measurements: one machine, one connection, one moment, cold cache. They describe the page, not field experience.

---

## Findings

### 49ef4a232e3e — 3.9 MB unresized hero image drives mobile LCP to 5.8s
- **Severity:** P1
- **So what:** Mobile visitors wait 5.8s for the largest element to paint — outside Google's "poor" threshold (>4.0s) — and every visitor downloads 3.9 MB for an image shown at a fraction of its size.
- **Framework tags:** Tier1-LCP, Tier2-image-hygiene
- **Flow:** measure:index:mobile
- **Locator:** http://localhost:8765/assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - `hero.png` delivered at 3000×2000 (3,900,000 bytes), displayed at 350×233 on mobile and 600×400 on desktop — over 99% of delivered pixels are discarded on mobile.
  - Homepage mobile LCP measures 5,800 ms (poor); desktop LCP on the same page measures 2,100 ms (good) because the smaller viewport still downloads the full 4.1 MB page but paints proportionally faster on this unthrottled connection.
  - Homepage total page weight is 4,104,000 bytes on both viewports — over the ~4 MB P1 threshold — driven almost entirely by this one asset (95% of page weight).
- **Evidence:** `measure/index-mobile.json:13,20,44-53` · `measure/index-desktop.json:20,44-53` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load `http://localhost:8765/` cold on a 390×844 viewport.
  2. Observe LCP candidate is the hero image at `assets/generated/hero.png`.
  3. Inspect network log: `hero.png` transfers 3,900,000 bytes at natural size 3000×2000.
- **Fix:** Resize and re-encode the hero image to its largest displayed size (600×400) and serve responsive variants (e.g. `srcset`) for mobile; convert to WebP/AVIF.

### 36e5bd5bb20c — Render-blocking stylesheets delay homepage mobile FCP to 2.9s
- **Severity:** P2
- **So what:** Mobile visitors see a blank screen for 2.9s before anything paints, because two stylesheets in `<head>` must finish before render starts.
- **Framework tags:** Tier1-FCP, Tier2-render-blocking
- **Flow:** measure:index:mobile
- **Locator:** http://localhost:8765/style.css
- **Personas hit:** n/a
- **Observed:**
  - `render_blocking` lists `https://fonts.example-cdn.test/all.css` (62,464 bytes) and `http://localhost:8765/style.css` on the homepage, both viewports.
  - Homepage mobile FCP is 2,900 ms ("needs improvement" band, ≤3.0s); desktop FCP on the same page is 900 ms (good).
  - The pricing page loads the same `style.css` render-blocking but is unaffected (FCP 500–800 ms) because the page carries no large competing asset — isolating the hero image, not the CSS, as the dominant cost, with the blocking CSS as a secondary, additive delay.
- **Evidence:** `measure/index-mobile.json:63-66` · `measure/index-desktop.json:63-66`
- **Repro:**
  1. Load `http://localhost:8765/` cold on a 390×844 viewport.
  2. Inspect `<head>`: two synchronous stylesheet links block first paint.
- **Fix:** Inline critical CSS, defer the webfont stylesheet with `media="print" onload`, and self-host or preconnect to the fonts CDN.

### 526700d2132e — Homepage and pricing assets served uncompressed with no cache headers
- **Severity:** P2
- **So what:** Every visit re-transfers the same bytes at full size instead of a compressed body or a cached copy, adding avoidable transfer time on every page and every repeat visit.
- **Framework tags:** Tier2-compression, Tier2-cache-headers
- **Flow:** measure:index:desktop
- **Locator:** http://localhost:8765/style.css
- **Personas hit:** n/a
- **Observed:**
  - `style.css` and the HTML document itself appear in `uncompressed_text_resources` on both `/` and `/pricing.html`, all viewports — no gzip/br content-encoding.
  - `missing_cache_headers` lists `style.css` on both pages and `hero.png` on the homepage — no `cache-control` on static assets that never change per-request.
- **Evidence:** `measure/index-desktop.json:55-62` · `measure/pricing-desktop.json:30-36`
- **Repro:**
  1. Request `http://localhost:8765/style.css` and inspect response headers.
  2. Confirm no `content-encoding` and no (or trivially short) `cache-control`.
- **Fix:** Enable gzip/br compression for text responses and add long-lived `cache-control: max-age` plus a cache-busting filename scheme for `style.css` and `hero.png`.

### e1b9637631e3 — Homepage throws a ReferenceError before load completes
- **Severity:** P3
- **So what:** A JavaScript error fires on every homepage load, on both viewports, before hygiene checks even reach interaction.
- **Framework tags:** Tier3-console-errors
- **Flow:** measure:index:desktop
- **Locator:** http://localhost:8765/
- **Personas hit:** n/a
- **Observed:**
  - `console_errors_on_load` records `"ReferenceError: nimbusBootstrap is not defined"` on both the desktop and mobile homepage measurements; the pricing page has no console errors.
- **Evidence:** `measure/index-desktop.json:84-86` · `measure/index-mobile.json:84-86`
- **Repro:**
  1. Load `http://localhost:8765/` cold with devtools console open.
  2. Observe `ReferenceError: nimbusBootstrap is not defined` logged before load settles.
- **Fix:** Find the missing `nimbusBootstrap` reference (likely a script load-order or removed dependency) and either define it or remove the dead call.

---

## Dropped for want of evidence
- None.

## For other lenses
- None — the console error above is a hygiene signal only; a functional consequence of `nimbusBootstrap`, if any, is for the `bugs` lens to assess.

## Coverage gaps
- Only `/` and `/pricing.html` were measured; no other pages in the site were captured under Mode B.
- No throttled-network measurement was taken — all numbers are this machine's own connection, unthrottled.

## Appendices
- A. Persona debriefs — n/a, this lens has no personas
- B. Session timelines — n/a, single-shot measurements per `measure/*.json`
- C. Screenshot index — `measure/screenshots/index-desktop.png`, `index-mobile.png`, `pricing-desktop.png`, `pricing-mobile.png`
