# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

> **⚠ Personas are INFERRED (`persona_mode: generic`).** Both visitors were invented by the agent, not researched. Findings rest on inferred motives.

## Method
- Framework: the four trust questions (Is this real? · What does it cost? · Who is behind it? · What happens to my data?) plus claim quality and consistency
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (evaluator, desktop 1440×900 · sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Not a compliance review: nothing here judges whether the privacy policy is legally sufficient

---

## Findings

### 03eb5087e09d — Cookie bar says no tracking while the privacy page says cookies and a third-party analytics call fires
- **Severity:** P0
- **So what:** The first promise the site makes about data is contradicted by its own pages; the sceptic left over it and the evaluator's trust was "undone".
- **Framework tags:** data-handling, consistency
- **Flow:** shape_v1
- **Locator:** /index.html#cookie
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Banner on landing reads "We use no tracking cookies on this site." (both devices).
  - Privacy page reads "We use cookies and similar technologies." and "We may share information with partners and service providers".
  - Both network logs show `GET https://analytics.example-tracker.test/t.js → 200 (third-party)` and `POST …/collect?uid=… → 204` on the landing page.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/screenshots/06-privacy.png` · `persona-sceptic/screenshots/01-privacy.png` · `persona-evaluator/network-full.txt:4-5` · `persona-sceptic/network-full.txt:2-3` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10` · `persona-sceptic/session.log:14` · DOM `crawl/html/1-index.html:37`: `<div id="cookie">We use no tracking cookies on this site.`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." — sceptic
  > "The privacy page and the cookie bar contradicting each other undid that." — evaluator, Q5
- **Repro:**
  1. Open `/` in a fresh context; read the bottom bar.
  2. Watch network: a third-party analytics script loads and posts a `uid` to `/collect`.
  3. Open `/privacy.html` from the footer; read "We use cookies and similar technologies."
- **Fix:** Either remove the analytics tag or rewrite the bar to name the analytics provider and what it collects, matching the privacy page word for word.
- Ambiguity: the capture does not record whether a cookie was set; P0 is chosen because the persona-visible contradiction alone drove an exit.

### 565842f4d37f — Privacy page names no partners, so the sceptic left without knowing who gets her notes
- **Severity:** P1
- **So what:** The sceptic came to learn what happens to her notes; the page could not tell her, and she left at 02:40.
- **Framework tags:** data-handling
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - The whole policy is four sentences; it names no partner, no processor, no data category beyond "information you provide".
  - "We may update this policy at any time." with no date or version shown.
  - Contact route is "Questions? Use the demo form." — no privacy contact.
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-sceptic/session.log:14` · `persona-sceptic/timeline.json` (`shape_v4.verdict`: "left; data handling unclear") · DOM `crawl/html/5-privacy.html:10`
  > "'We may share information with partners and service providers.' With whom? Not said. … That's not a privacy policy, that's a shrug."
  > "Leave. … the privacy page won't say who the partners are." — Q3
- **Repro:**
  1. On mobile, open `/` and tap Privacy in the footer.
  2. Look for a named partner, data list, or privacy contact. None appears.
- **Fix:** List each partner and service provider by name with what it receives, add a last-updated date and a privacy contact email.

### 191f39082ce0 — Privacy page names no partners, leaving the evaluator unsure about handing over data
- **Severity:** P2
- **So what:** The evaluator did not leave over this, but "Data, unsure" blocks taking the tool to a team.
- **Framework tags:** data-handling
- **Flow:** shape_v3
- **Locator:** /privacy.html#evaluator
- **Personas hit:** evaluator
- **Observed:**
  - Read the same four-sentence policy at 04:50.
  - Listed "Who are the partners you share data with?" among unanswered questions.
  - Exit reason was price, not data (`session.log:29`).
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/timeline.json` (`questions_unanswered`) · `persona-evaluator/persona-debrief.md` Q5
  > "Which partners? It doesn't say."
  > "Data, unsure." — Q5
- **Repro:**
  1. On desktop, open `/privacy.html` from the footer.
  2. Look for named partners. None appears.
- **Fix:** Same change as the sceptic variant: name partners, what each receives, and a dated policy.

### c45f461c2f5e — No price on the pricing page; every plan says "Contact sales"
- **Severity:** P1
- **So what:** The evaluator came to learn the cost, could not, and would not proceed or trust them with money.
- **Framework tags:** pricing-transparency
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise each show only a "Contact sales" button; no currency figure anywhere.
  - The only explanation: "Pricing depends on your workspace type and sync topology." — terms the evaluator could not apply to himself.
  - Gave up on price at 02:30; verdict "would not proceed; no price".
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/session.log:29` · `persona-evaluator/timeline.json` (`price_found: false`, `objectives[0].gave_up: true`)
  > "Every plan says Contact sales. No numbers anywhere."
  > "Money, no — I don't know what they'd charge." — Q5
- **Repro:**
  1. Open `/`, click Pricing in the nav.
  2. Look for a number on any plan. None appears.
- **Fix:** Show a per-seat or per-month price on Starter and Team; keep "Contact sales" only on Enterprise.

### 39f6f364ed63 — Testimonials carry no names, so the only social proof was disbelieved
- **Severity:** P2
- **So what:** The site's only proof that anyone uses the product actively lowered belief; nothing replaced it.
- **Framework tags:** proof
- **Flow:** shape_v2
- **Locator:** /index.html#loved-by-teams
- **Personas hit:** evaluator
- **Observed:**
  - "Loved by teams" shows three quotes attributed "— a happy customer", "— a user", "— anonymous".
  - No customer name, company, logo or number anywhere the evaluator went.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15` · `persona-evaluator/timeline.json` (`trust_down`: "Anonymous testimonials")
  > "Three quotes, nobody has a name. I don't believe these."
- **Repro:**
  1. Open `/` on desktop and scroll to "Loved by teams".
  2. Read the attributions.
- **Fix:** Replace the three quotes with named people, their company, and one specific outcome each — or remove the section.

### e3e6490bbfaf — Demo form demands a phone number before the visitor has seen the product
- **Severity:** P2
- **So what:** The only route to a price asks for a phone number up front; the evaluator backed out, a less patient visitor reads it as a sales trap.
- **Framework tags:** data-handling, pricing-transparency
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - "Contact sales" on every plan leads to the home-page demo form.
  - Seven fields; "Phone number" is `required`.
  - Evaluator backed out at 03:15 without submitting.
- **Evidence:** `persona-evaluator/session.log:20-22` · `persona-evaluator/timeline.json` (`trust_down`: "Phone number required for a demo") · DOM `crawl/html/1-index.html:31`: `<label>Phone number</label><input type="tel" required>` · `persona-evaluator/screenshots/03-demo-form.png` (captured blank — see Coverage gaps)
  > "Seven fields. Phone required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Open `/pricing.html`, click any "Contact sales".
  2. Count required fields on the demo form.
- **Fix:** Drop the phone field or make it optional, and say on the form why each field is asked for.

### 7910178489b2 — Data location and company details sit only on About, not where visitors look for them
- **Severity:** P2
- **So what:** The site's strongest trust material was found late by one persona and by luck by the other; most visitors never open About.
- **Framework tags:** provenance, data-handling
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About names Priya Raman, founded 2023, eight people, "14 Harbourside Walk, Bristol", company number 14482201.
  - FAQ: "In the EU (Frankfurt) by default." — absent from the Privacy page.
  - Both personas logged this as the main trust lift; neither saw it on home or privacy pages.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-12`
  > "That's the answer I wanted and it's on the About page, not the Privacy page." — sceptic
  > "Those are actual answers. Why isn't this on the home page?" — evaluator
- **Repro:**
  1. Open `/privacy.html`: no storage location.
  2. Open `/about.html`: storage location and company details present.
- **Fix:** Copy the Frankfurt storage answer into the privacy page and put founder, location and company number in the home-page footer.

### fad218c2a42b — "See it in action" does nothing, so the product never visibly exists
- **Severity:** P2
- **So what:** Neither persona saw the product work; "remembers everything" stays an unproven claim.
- **Framework tags:** proof, claim-quality
- **Flow:** shape_v2
- **Locator:** /index.html#see-it-in-action
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator clicked twice at 00:40; nothing happened.
  - Sceptic tapped it at 02:20 wanting to see it "remember"; nothing happened.
  - No screenshot, video or demo of the product appears on any page visited.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/timeline.json` (`trust_down`: "'See it in action' does nothing")
  > "'It remembers everything.' No — nothing on the site shows it remembering anything; the button that might have doesn't work." — sceptic, Q6
- **Repro:**
  1. Open `/`, click "See it in action".
  2. Observe no navigation or change.
- **Fix:** Point "See it in action" at a 30-second product clip or screenshot sequence showing a note being recalled.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Analytics script may set a cookie before the OK click — network log has no timestamps or Set-Cookie headers.
- "zero-knowledge vault, so nothing you write is ever … exposed" may clash with "share information with partners" — no persona connected the two.

## For other lenses
- "Features" nav link returns 404 (`persona-evaluator/screenshots/04-features-404.png`) — technical / conversion.
- Hero copy "bi-directional sync graph with a zero-knowledge vault" not understood — clarity.
- Newsletter box outweighs the primary button — conversion.
- `hero.png` is 3.9 MB — technical.

## Coverage gaps
- `persona-evaluator/screenshots/03-demo-form.png` is blank; form contents rest on `session.log` and the crawl DOM.
- Sceptic never opened Pricing, so a price-severity flip could not be observed.
- No terms page visited; no persona on a post-consent reload, so banner-before/after behaviour is unmeasured.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06 · sceptic 00–02
