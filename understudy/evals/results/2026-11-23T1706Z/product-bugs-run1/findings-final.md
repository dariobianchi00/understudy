# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: bug report — console, network, dead ends, broken states, lying feedback, state corruption
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 51982df643b2 — Saving a note fails with POST /api/notes 500 and nothing is stored
- **Severity:** P0
- **So what:** Every note a user writes is lost; both personas abandoned with zero notes saved.
- **Framework tags:** failed-request, data-loss
- **Flow:** write-and-find-note
- **Locator:** POST /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - Save returns HTTP 500 on every attempt (3 of 3 across both personas).
  - Dashboard still shows "Nothing here yet." and search finds nothing afterwards.
  - Both personas said they would not keep using the product.
- **Evidence:** `persona-novice/console-full.txt:3` · `persona-novice/console-full.txt:5` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-power-user/network-full.txt:3` · `persona-novice/session.log:18`
  > "[error] new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)"
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/new.html` · build `fixture02` · `[03:05]` (also `[03:50]`; power-user `[01:00]`)
- **Expected:** POST /api/notes returns 2xx; the note appears on the dashboard and in search.
- **Actual:** `POST http://localhost:8765/api/notes → 500 internal error`; dashboard "Nothing here yet."; search "No results for 'Dentist'."
- **Repro:**
  1. Complete signup (workspace type any) and land on `/app/dashboard.html`.
  2. Open "New block" (`/app/new.html`); enter title "Dentist" and a few lines of body.
  3. Click Save; observe 500 in network log.
  4. Return to dashboard and search "Dentist"; note is absent.
- **Fix:** Fix the server error in the `/api/notes` handler and log the stack trace; add a regression test that a saved note is listed.

### 8c1bcaf5691b — Saved toast shows after POST /api/notes returned 500
- **Severity:** P0
- **So what:** The user is told the note is safe while it is lost; they stop trusting every other confirmation.
- **Framework tags:** lying-feedback
- **Flow:** write-and-find-note
- **Locator:** /app/new.html#save-toast
- **Personas hit:** novice, power-user
- **Observed:**
  - Green "Saved ✓" toast appears top right, then the page redirects to the dashboard.
  - The same request returned 500, so the success path ignores the response status.
  - Novice wrote the note twice before concluding "It is lying to me."
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-novice/network-full.txt:5`
  > "Green "Saved ✓" popped up top right."
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/new.html` · build `fixture02` · `[03:05]` (also `[03:50]`; power-user `[01:00]`)
- **Expected:** An error message and the form kept intact when the save fails; "Saved ✓" only after a 2xx.
- **Actual:** "Saved ✓" toast, redirect to dashboard, input discarded. The toast itself is not in `persona-novice/screenshots/04-note-saved-toast.png` (captured before Save); evidence is session.log.
- **Repro:**
  1. Open `/app/new.html`; enter title and body.
  2. Click Save while POST /api/notes returns 500.
  3. Observe "Saved ✓" toast and redirect; form content is gone.
- **Fix:** In the new.html save handler, show the toast only on `response.ok`; on failure show an error and keep the draft.

### 6417302498d3 — Memories page lists facts the user never entered, with no notes saved
- **Severity:** P1
- **So what:** A new user is shown false claims about themselves, which makes them doubt the Saved toast too.
- **Framework tags:** broken-state, data-integrity
- **Flow:** write-and-find-note
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Page lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer reads "Memories are built from your notes and connected accounts." Zero notes were stored and none connected.
  - Power-user assumed "a demo panel"; novice asked "is it making up the 'Saved' too?"
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist."
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/memories.html` · build `fixture02` · `[04:30]` (power-user `[02:30]`)
- **Expected:** Empty state, or only memories derived from the user's own notes.
- **Actual:** Three memories shown to a brand-new workspace. Source is unknown: seeded demo data or another account's data (cannot tell from logs).
- **Repro:**
  1. Create a new workspace; do not save any note (saving fails anyway).
  2. Click "Memories" in the top nav.
  3. Observe the three memories above.
- **Fix:** Show an empty state until memories derive from the user's notes; remove hardcoded or shared seed data from the memories endpoint.

### c4ef89658864 — Dashboard throws ReferenceError renderGraphOverlay is not defined on every load
- **Severity:** P2
- **So what:** A script on the main screen crashes each load; the effect is unconfirmed, but it may be why the list stays empty.
- **Framework tags:** console-error
- **Flow:** write-and-find-note
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Error logged on 4 of 4 dashboard loads (novice) and 2 of 2 (power-user).
  - No visible breakage was attributable to it; the empty list is explained by the 500.
  - Possibly tied to the "Federated graph replication" setting chosen at signup.
- **Evidence:** `persona-novice/console-full.txt:1` · `persona-novice/console-full.txt:4` · `persona-power-user/console-full.txt:1` · `persona-novice/screenshots/02-dashboard-empty.png`
  > "[error] dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined"
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/dashboard.html` · build `fixture02` · `[00:55]`
- **Expected:** Dashboard loads with no console errors.
- **Actual:** `Uncaught ReferenceError: renderGraphOverlay is not defined` on each load.
- **Repro:**
  1. Complete signup and open `/app/dashboard.html`.
  2. Open the browser console; error appears on load.
- **Fix:** Define or import `renderGraphOverlay` in dashboard.html, or remove the call when the graph feature is off.

---

## Dropped for want of evidence
- Search returns no results for saved notes — no note was ever stored, so search itself is untested.
- Whether the "Saved ✓" toast fires in a second browser tab — not exercised.

## For other lenses
- Signup forces an irreversible "Federated graph / Sovereign vault / Hybrid mesh" choice with no explanation — ux, onboarding.
- Nav says "Cards" and "New block" for what users call notes — content.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux.
- Settings jargon "Vault attestation", "Enable webhook sync" — content.

## Coverage gaps
- Edit, delete, export and webhook sync never exercised.
- Only desktop 1440×900; no mobile device.
- Note retrieval never reached, since saving fails.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
