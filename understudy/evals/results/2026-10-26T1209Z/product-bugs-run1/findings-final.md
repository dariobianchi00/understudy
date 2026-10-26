# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: bug report — console, network, dead ends, broken states, lying feedback, state corruption
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 3710b17ec0fd — Saving a note fails with HTTP 500 and the note is lost
- **Severity:** P0
- **So what:** Every note a user writes is discarded; the core job (write a note, find it again) cannot be done.
- **Framework tags:** broken-state, failed-request, data-loss
- **Flow:** shape_2
- **Locator:** POST /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST /api/notes` returned 500 on all 3 attempts (novice 03:05 and 03:50, power-user 01:00).
  - Dashboard stayed at "Nothing here yet." after each save.
  - Searching the saved titles ("Dentist", "Roadmap") returned no results.
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/new.html` · build `n/a (not recorded)` · `[03:05]`; also persona `power-user` · desktop-1440x900 · same URL · `[01:00]`
- **Expected:** Save persists the note; the dashboard lists it and search finds it.
- **Actual:** `[error] new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)`; network entry `[POST] http://localhost:8765/api/notes → 500 internal error  (03:05)`.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-novice/console-full.txt:3` · `persona-power-user/network-full.txt:3` · `persona-novice/session.log:17`
  > "Save doesn't save and search doesn't search."
- **Repro:**
  1. Sign in and create a workspace at `/app/signup.html`; land on `/app/dashboard.html`.
  2. Click "New block"; enter title "Dentist" and a few lines of body.
  3. Click Save; watch Network for `POST /api/notes`.
  4. Observe 500, return to dashboard: "Nothing here yet." Server-side cause not visible in captures.
- **Fix:** Fix the server error in the `/api/notes` create handler; add an API test asserting 201 and the note appearing in the list.

### ad1c10f1799f — Success toast "Saved ✓" shows although the save request failed
- **Severity:** P0
- **So what:** Users believe lost work is stored and only find out later; both personas stopped trusting the product.
- **Framework tags:** lying-feedback
- **Flow:** shape_2
- **Locator:** new.html Saved toast
- **Personas hit:** novice, power-user
- **Observed:**
  - Green "Saved ✓" appeared at 03:05 and 03:50 (novice) and 01:00 (power-user), each paired with a 500.
  - Page then returned to the dashboard as if the save succeeded.
  - Screenshot `04-note-saved-toast.png` shows an empty New block form and no toast; the toast is evidenced by log text only.
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/new.html` · build `n/a (not recorded)` · `[03:05]`; also persona `power-user` · desktop-1440x900 · same URL · `[01:00]`
- **Expected:** An error message, with the user's input kept in the form, when the request fails.
- **Actual:** Toast "Saved ✓" and redirect to dashboard, with `POST /api/notes → 500 internal error`.
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-novice/network-full.txt:5`
  > "It said saved." / "It is lying to me."
- **Repro:**
  1. Open `/app/new.html` after signup.
  2. Enter title "Dentist" and body text; click Save.
  3. Observe "Saved ✓" top right and redirect to dashboard.
  4. Compare with Network: `POST /api/notes` is 500. Toast and redirect fire regardless.
- **Fix:** Show the toast and redirect only on a 2xx from `POST /api/notes`; on failure show an error and keep the form contents.

### d8b64bc3a61b — Memories page shows three facts the user never supplied
- **Severity:** P1
- **So what:** Invented personal facts make users suspect every other claim, including "Saved", and undermine the "remembers everything" promise.
- **Framework tags:** broken-state, lying-feedback
- **Flow:** surfaces
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Page lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer says "Memories are built from your notes and connected accounts."
  - Neither persona had saved a note or connected an account; both said the content was not theirs.
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/memories.html` · build `n/a (not recorded)` · `[04:30]`; also persona `power-user` · desktop-1440x900 · same URL · `[02:30]`
- **Expected:** An empty state, or memories derived from the user's own notes and connected accounts.
- **Actual:** Three hard-coded-looking statements shown as "What Nimbus remembers about you".
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist."
- **Repro:**
  1. Create a new workspace; save no notes (saving fails anyway) and connect no accounts.
  2. Click "Memories" in the top nav.
  3. Observe the three statements. Source of the data not determinable from captures.
- **Fix:** Show an empty state on `/app/memories.html` until memories are generated from the user's own data; remove the seeded or demo entries.

### 2f619bb57336 — Dashboard throws "renderGraphOverlay is not defined" on every load
- **Severity:** P2
- **So what:** An undefined function on the main screen signals a half-shipped feature; it may be why the card list never renders.
- **Framework tags:** console-error
- **Flow:** shape_1
- **Locator:** dashboard.html renderGraphOverlay
- **Personas hit:** novice, power-user
- **Observed:**
  - Console shows the error 4 times for novice and 2 times for power-user, one per dashboard visit.
  - No user-visible effect was tied to it; the empty list is already explained by the 500 on save.
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/dashboard.html` · build `n/a (not recorded)` · `[00:55]`; also persona `power-user` · desktop-1440x900 · same URL · `[00:30]`
- **Expected:** Dashboard loads with no uncaught exceptions.
- **Actual:** `[error] dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined`
- **Evidence:** `persona-novice/console-full.txt:1` · `persona-novice/console-full.txt:4` · `persona-power-user/console-full.txt:1`
- **Repro:**
  1. Sign in and open `/app/dashboard.html`.
  2. Open the browser console.
  3. Observe the `ReferenceError` on each load.
- **Fix:** Define or import `renderGraphOverlay` in `dashboard.html`, or remove the call if the feature is not shipped.

---

## Dropped for want of evidence
- Search returns nothing for saved notes — cannot be separated from the save failure; no note ever existed to search for.
- Toast visibly rendered on screen — `04-note-saved-toast.png` shows no toast; it is cited from log text only.

## For other lenses
- Signup forces an irreversible choice between "Federated graph", "Sovereign vault" and "Hybrid mesh" with no explanation — ux/content.
- Dashboard empty state "Nothing here yet." gives no next step — onboarding.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux.
- Settings jargon "Vault attestation", "Enable webhook sync" is unexplained — content.
- Nav says "Cards" and "New block" for what users call notes — content.

## Coverage gaps
- Note list, open, edit and delete never reached because no note persisted.
- Export (Markdown) was seen but never run; output unverified.
- Mobile viewport not tested; both personas used desktop-1440x900.
- Build id not recorded in the run folder.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
