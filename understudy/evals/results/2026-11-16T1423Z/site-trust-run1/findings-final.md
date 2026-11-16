# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four trust questions — is this real · what does it cost · who is behind it · what happens to my data
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900 · sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Findings cover only what the personas could check on the site. This is not a compliance review.

---

## Findings

### b509d2e18cb6 — Cookie bar claims no tracking cookies while an analytics tracker fires before consent
- **Severity:** P0
- **So what:** The site's first trust claim is contradicted by its own privacy page and its own network traffic, and both personas noticed the contradiction.
- **Framework tags:** data-handling, consistency, cookie-banner-mismatch
- **Flow:** shape_1
- **Locator:** #cookie
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Banner reads "We use no tracking cookies on this site." Its OK button only removes the banner (`crawl/html/1-index.html:37`).
  - `analytics.example-tracker.test/t.js` is loaded unconditionally in `<head>` and POSTs `/collect?uid=…` for both personas.
  - Privacy page says "We use cookies and similar technologies." Both personas called out the contradiction.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/network-full.txt` · `persona-sceptic/network-full.txt` · `persona-evaluator/screenshots/06-privacy.png` · `persona-sceptic/screenshots/01-privacy.png` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10` · DOM `crawl/html/1-index.html:3`: `<script src="https://analytics.example-tracker.test/t.js" async></script>`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." (sceptic)
  > "The cookie bar said no tracking. This page says they use cookies and share with partners. Which is it?" (evaluator)
- **Repro:**
  1. Open `/` in a fresh context with network logging on.
  2. Read the bottom banner: "We use no tracking cookies on this site."
  3. Before you click OK, see the GET to `analytics.example-tracker.test/t.js` and the POST to `/collect?uid=…` → 204.
  4. Open `/privacy.html` and read "We use cookies and similar technologies."
- **Fix:** Rewrite the banner to name the analytics tracker and offer a choice, and load `t.js` only after consent.
- **Ambiguity:** The network log has no cookie headers, so it shows a tracker sending a uid, not a cookie being set. This is rated P0 because the banner, the privacy page and the observed traffic disagree.

### 90cc492bf499 — Pricing page shows no price on any plan, only Contact sales
- **Severity:** P1
- **So what:** The evaluator came to find the price, could not, and said they would look for an alternative. Money trust: "no".
- **Framework tags:** pricing-transparency
- **Flow:** shape_3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise each show only "Contact sales". The page has no numbers.
  - The only explanation given is "Pricing depends on your workspace type and sync topology." The evaluator could not map either term to themselves.
  - Objective "find out what it costs without giving an email": `gave_up: true` at 02:30 after checking `/pricing.html` and `/index.html#demo`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17` · `persona-evaluator/session.log:18` · `persona-evaluator/session.log:19` · `persona-evaluator/session.log:29` · `persona-evaluator/timeline.json` (`price_found: false`, `objectives[0].gave_up: true`)
  > "Money, no — I don't know what they'd charge."
- **Repro:**
  1. Open `/pricing.html`.
  2. Look for a number on any of the three plans. There is none.
  3. Click "Contact sales". It goes to the home-page demo form.
- **Fix:** Show a price or a starting price on Starter and Team, and replace "workspace type and sync topology" with the actual pricing unit.

### fcce4a1e78c6-a — Privacy page names no partners and reserves unannounced changes
- **Severity:** P1
- **So what:** The sceptic came to find out what happens to their notes. This page is why they left.
- **Framework tags:** data-handling, third-parties-unnamed
- **Flow:** shape_3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - The full policy is four sentences: "We may share information with partners and service providers to improve your experience."
  - The page names no partners and lists nothing about what is collected beyond "information about how you use the service". It says "We may update this policy at any time."
  - The sceptic left at 02:40 (`left_early: true`). Verdict: "left; data handling unclear".
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-sceptic/session.log:14` · `persona-sceptic/timeline.json` (`left_early: true`)
  > "That's not a privacy policy, that's a shrug."
  > "The About page made them real … The privacy page took it back."
- **Repro:**
  1. On mobile, tap Privacy in the footer.
  2. Look for the names of the partners or third parties. None are given.
- **Fix:** On `/privacy.html`, name each third party and what it receives, list what is collected, and explain how changes are announced.

### fcce4a1e78c6-b — Privacy page names no partners and reserves unannounced changes
- **Severity:** P2
- **So what:** The evaluator's data trust fell to "unsure". It was not the reason they left (price was), but it undid the trust the About page had built.
- **Framework tags:** data-handling, third-parties-unnamed
- **Flow:** shape_3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - Read at 04:50: "We may share information with partners and service providers." The evaluator asked "Which partners?"
  - Listed under Q4 as a question the site never answered: "Who they share my data with."
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/persona-debrief.md` (Q4, Q5)
  > "Data, unsure. The About page made them feel real (a named founder, an address). The privacy page and the cookie bar contradicting each other undid that."
- **Repro:**
  1. On desktop, click Privacy in the footer.
  2. Look for the names of the partners. None are given.
- **Fix:** Same as -a: name the partners on `/privacy.html`.

### b313566f0a96 — All three testimonials are anonymous, so the only proof on the home page was disbelieved
- **Severity:** P2
- **So what:** The only social proof on the home page actively lowered belief instead of raising it.
- **Framework tags:** proof, claim-quality
- **Flow:** shape_2
- **Locator:** /index.html — Loved by teams
- **Personas hit:** evaluator
- **Observed:**
  - "Loved by teams" shows three quotes attributed to "— a happy customer", "— a user" and "— anonymous".
  - None has a name, company or number attached. The evaluator listed "Anonymous testimonials" under `trust_down`.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15`
  > "Nobody has a name. I don't believe these."
- **Repro:**
  1. Scroll `/` to "Loved by teams".
  2. Read the attributions.
- **Fix:** Replace the three quotes with one or two from named customers, with their role and company, or remove the section.

### 3d29773146d5 — Demo form requires a phone number before any price or product is shown
- **Severity:** P2
- **So what:** The evaluator was asked for a phone number before getting anything in return, and backed out. The risk is that visitors lose trust before the first contact.
- **Framework tags:** data-handling, value-exchange
- **Flow:** shape_3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - "Contact sales" on every plan leads to a seven-field form. Phone number is `required`.
  - The evaluator backed out at 03:15 without submitting. The capture screenshot `03-demo-form.png` is blank, so the DOM is cited instead.
- **Evidence:** `persona-evaluator/session.log:21` · `persona-evaluator/session.log:22` · DOM `crawl/html/1-index.html:31`: `<label>Phone number</label><input type="tel" required>`
  > "Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. On `/pricing.html`, click any "Contact sales".
  2. Look at the form: seven fields, and Phone number is required.
- **Fix:** Make the phone field optional on the demo form, and don't make the form the only route to a price.

### c131ae1c352d — Founder, address and data location appear only on the About page
- **Severity:** P2
- **So what:** This was the strongest trust signal on the site, and both personas found it only after trust had already started to fall.
- **Framework tags:** provenance, data-handling
- **Flow:** shape_3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About lists "Priya Raman", "14 Harbourside Walk, Bristol", "Company number 14482201", "eight people", "2023", and data "In the EU (Frankfurt) by default".
  - Both personas named this as their main reason to trust the site. It reached them at 03:50 (evaluator) and 01:30 (sceptic).
  - The data-location answer is not on the Privacy page. The sceptic noticed.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "That's the answer I wanted and it's on the About page, not the Privacy page."
  > "Why isn't this on the home page?"
- **Repro:**
  1. Open `/`. It shows no company name, place or person.
  2. Open `/about.html`. All of them are there.
- **Fix:** Add a home-page line naming the founder, Bristol and Frankfurt storage, and copy the Frankfurt answer into `/privacy.html`.

### 27f8caa7dfe8 — No product is shown working, and the one demo button does nothing
- **Severity:** P2
- **So what:** "Is this real?" had no product answer. Neither persona saw the promised "remembers everything" behaviour.
- **Framework tags:** proof, claim-quality
- **Flow:** shape_2
- **Locator:** See it in action
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" did nothing on desktop (two clicks) or mobile. The console shows `Uncaught ReferenceError: nimbusBootstrap is not defined`.
  - The hero image is an abstract illustration, not a product screen. The sceptic listed the dead button under `trust_down`.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/console-full.txt`
  > "'It remembers everything.' No — nothing on the site shows it remembering anything; the button that might have doesn't work."
- **Repro:**
  1. Open `/`.
  2. Click "See it in action". Nothing happens.
- **Fix:** Wire "See it in action" to a short screen recording of a note being recalled, and put a real product screenshot in the hero.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether the tracker sets a cookie: the network log has no `Set-Cookie` or cookie headers. Capture them next run.
- The hero subhead "nothing you write is ever … exposed" next to "share information with partners": neither persona reacted to the pairing, so it is unrated.
- The sceptic's view of pricing: they never looked, so pricing trust for that persona is unobserved.

## For other lenses
- "Features" in the nav returns a 404 (`persona-evaluator/screenshots/04-features-404.png`) — technical / conversion
- "See it in action" is dead because `nimbusBootstrap` is not defined — technical
- The headline does not say what the product is, and "bi-directional sync graph" / "zero-knowledge vault" are jargon — clarity
- The newsletter box outweighs the primary button, and the seven-field form is the only path to a trial — conversion
- The 3.9 MB hero image and render-blocking third-party CSS — technical

## Coverage gaps
- The sceptic did not visit `/pricing.html`.
- The evaluator's demo-form screenshot (`03-demo-form.png`) is blank.
- No cookie or storage inspection was done. The network log has no timestamps relative to the OK click.
- No terms page was visited, and none was seen linked in the footer.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06 · sceptic 00–02
