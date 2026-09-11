# Nimbus Notes — technical findings — Run 2026-09-08 (fixture01)

## Method
- Framework: technical-metrics.md — Tier 1 Core Web Vitals, Tier 2 delivery, Tier 3 hygiene
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens, `Flow` is `measure:<page>:<viewport>`
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Conditions verified before use: all four measurements have `viewport_verified: true`, `cache: cold`, `throttling: none`, `runs: 1`

---

## Findings

### 46ae46260c35 — Unoptimized 3.9MB hero image drives page weight to 4.1MB and mobile LCP to 5.8s
- **Severity:** P1
- **So what:** Mobile visitors — the majority on a marketing homepage — wait 5.8s for the largest visible element to appear, in Google's "poor" band.
- **Framework tags:** Tier 1 (LCP), Tier 2 (image hygiene, page weight)
- **Flow:** measure:index:mobile
- **Locator:** http://localhost:8765/assets/generated/hero.png
- **Personas hit:** n/a
- **Observed:**
  - `hero.png` delivered at 3000×2000, displayed at 350×233 (mobile) and 600×400 (desktop) — roughly 73x more pixels than the mobile layout uses
  - Single file is 3,900,000 bytes, 95% of the page's 4,104,000-byte total weight
  - Mobile LCP measured 5.8s (poor, >4.0s threshold); desktop LCP on the identical asset measured 2.1s (good) — same payload, different viewport outcome
- **Evidence:** `measure/index-mobile.json:13-53` · `measure/index-desktop.json:13-53` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Load `http://localhost:8765/` at 390×844 with a cold cache
  2. Observe `largest-contentful-paint` timing and the `hero.png` network entry
- **Fix:** Re-encode `hero.png` to its largest displayed size (~600×400) and serve a responsive `srcset` so mobile gets a smaller file than desktop.

### 6ebe533ecd41 — Render-blocking font CSS and stylesheet delay mobile FCP on the homepage
- **Severity:** P2
- **So what:** Nothing paints on mobile until two render-blocking stylesheets finish, pushing first paint to 2.9s ("needs improvement" band).
- **Framework tags:** Tier 1 (FCP), Tier 2 (render-blocking, third-party weight)
- **Flow:** measure:index:mobile
- **Locator:** https://fonts.example-cdn.test/all.css
- **Personas hit:** n/a
- **Observed:**
  - `render_blocking` lists `https://fonts.example-cdn.test/all.css` (62,464 bytes, third-party) and `http://localhost:8765/style.css`, both unmarked async/defer
  - Mobile FCP measured 2.9s vs desktop 0.9s on the same two blocking resources
  - Third-party font CSS is the larger of the two: 62,464 of the page's 101,376 bytes of third-party weight
- **Evidence:** `measure/index-mobile.json:63-66` · `measure/index-desktop.json:63-66`
- **Repro:**
  1. Load `http://localhost:8765/` at 390×844 with a cold cache
  2. Inspect the resource waterfall for stylesheets loaded before first paint
- **Fix:** Preload or self-host the font CSS, and mark non-critical CSS with `media` scoping so it stops blocking first paint.

### 2846000eb507 — Static assets served without compression or cache headers
- **Severity:** P2
- **So what:** Every repeat visit and every text response re-downloads full-size bytes because neither compression nor caching is configured.
- **Framework tags:** Tier 2 (compression, cache headers)
- **Flow:** measure:index:mobile
- **Locator:** http://localhost:8765/style.css
- **Personas hit:** n/a
- **Observed:**
  - `style.css` and the HTML document itself ship with no `content-encoding` (no gzip/br) on both `/` and `/pricing.html`
  - `style.css` and `hero.png` have no `cache-control` header on `/`; `style.css` has none on `/pricing.html` either
  - Same two resources fail both checks on every page measured, not a one-off
- **Evidence:** `measure/index-mobile.json:55-62` · `measure/pricing-mobile.json:30-36`
- **Repro:**
  1. Request `http://localhost:8765/style.css` and inspect response headers
  2. Confirm no `content-encoding` and no `cache-control`
- **Fix:** Enable gzip/br on the web server for text responses and set `cache-control: max-age` on static assets (CSS, images).

### 00ee849a0fcf — Uncaught ReferenceError fires on every homepage load
- **Severity:** P3
- **So what:** A script fails before it does anything, on every homepage visit regardless of viewport — hygiene signal, not measured to affect load metrics here.
- **Framework tags:** Tier 3 (console errors on load)
- **Flow:** measure:index:mobile
- **Locator:** ReferenceError: nimbusBootstrap is not defined
- **Personas hit:** n/a
- **Observed:**
  - `console_errors_on_load` contains `"ReferenceError: nimbusBootstrap is not defined"` on both mobile and desktop measurements of `/`
  - `/pricing.html` has zero console errors on load in either viewport
- **Evidence:** `measure/index-mobile.json:84-86` · `measure/index-desktop.json:84-86`
- **Repro:**
  1. Load `http://localhost:8765/` with devtools console open
  2. Observe the `ReferenceError` before `load` fires
- **Fix:** Define or remove the `nimbusBootstrap` reference so the homepage loads without a console error.

---

## Dropped for want of evidence
None — every Tier 1/2/3 observation used here traces to a `measure/*.json` field.

## For other lenses
- Nothing to route — no copy, trust, or conversion claims observed in this evidence.

## Coverage gaps
- `/features.html`, `/about.html`, `/privacy.html` — present in `crawl/pages/` but never captured under `measure/`; no Tier 1/2/3 data for them this run.
- Only 1 run per page/viewport (`runs: 1`) — no repeat-measurement variance data.

## Appendices
- A. Persona debriefs — n/a, no-persona lens
- B. Session timelines — n/a, this lens reads `measure/*.json` directly
- C. Screenshot index — `measure/screenshots/index-mobile.png`, `measure/screenshots/index-desktop.png`, `measure/screenshots/pricing-mobile.png`, `measure/screenshots/pricing-desktop.png`
