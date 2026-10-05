# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: bug report — console, network, dead ends, broken states, lying feedback, state corruption
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### dfe7ca4e9df7 — Save shows "Saved ✓" while POST /api/notes returns 500, so every note is silently lost
- **Severity:** P0
- **So what:** Users lose every note while the UI says it worked; both personas quit with zero notes saved.
- **Framework tags:** lying-feedback, failed-request, data-loss
- **Flow:** write a note and find it again
- **Locator:** POST /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - Both saves returned 500, yet the persona saw a green "Saved ✓" and a redirect to the dashboard.
  - Dashboard still read "Nothing here yet."; search for the saved title returned "No results".
  - Reproduced 3 of 3 attempts (novice 03:05, novice 03:50, power-user 01:00).
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:16-19` · `persona-novice/console-full.txt:2` · `persona-novice/network-full.txt:5` · `persona-power-user/network-full.txt:3`
  > "[error] new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)"
  > "It said saved." / "It is lying to me."
  - Note: `04-note-saved-toast.png` shows an empty New block form and no toast; the toast is evidenced by the persona log only.
- **Repro:**
  1. Sign in, complete signup at `/app/signup.html` (any workspace type).
  2. Open "New block" (`/app/new.html`); title "Dentist", add a few lines of body.
  3. Click Save; green "Saved ✓" appears, page returns to dashboard.
  4. Observe the dashboard "Your cards" empty and POST `/api/notes` → 500 in the network log.
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/new.html` · build `unknown (not recorded)` · `[03:05]`; also `power-user` · desktop-1440x900 · same URL · `[01:00]`
- **Expected:** Save persists the note, it appears under "Your cards" and in search; on failure an error is shown and the form keeps the input.
- **Actual:** `POST http://localhost:8765/api/notes → 500 internal error` followed by "Saved ✓" and an empty list.
- **Fix:** In the `new.html` save handler, show "Saved ✓" and redirect only on a 2xx response, show an error and keep the form on failure, and fix the 500 in `/api/notes`.

### a21732575714 — Dashboard throws Uncaught ReferenceError: renderGraphOverlay is not defined on every load
- **Severity:** P2
- **So what:** A script error fires on each dashboard load; its user impact is unconfirmed, but it may break the cards list or overlay.
- **Framework tags:** console-error
- **Flow:** write a note and find it again
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Thrown 4 times for novice (4 dashboard loads) and 2 times for power-user.
  - No visible overlay on screen; the persona never mentioned it; cause of the empty list is attributed to the 500, not this error.
  - Cannot tell from the evidence whether any rendering depends on the missing function.
- **Evidence:** `persona-novice/console-full.txt:1` · `persona-power-user/console-full.txt:1` · `persona-novice/screenshots/02-dashboard-empty.png`
  > "dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined"
- **Repro:**
  1. Sign in and complete signup.
  2. Open `/app/dashboard.html` with the browser console open.
  3. Observe the ReferenceError on load. Repeats on each return to the dashboard.
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/dashboard.html` · build `unknown (not recorded)` · `[00:55]`
- **Expected:** Dashboard loads with no console errors.
- **Actual:** `dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined`
- **Fix:** Define or import `renderGraphOverlay` in `dashboard.html`, or remove the call, and guard the call so a failure cannot stop later rendering.

### dfc606a9a9f7 — Memories page asserts facts the user never provided, with no notes saved and no accounts connected
- **Severity:** P2
- **So what:** Invented "facts" about the user make both personas distrust the product, including its "Saved" message.
- **Framework tags:** broken-state, lying-feedback
- **Flow:** memories
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Three statements shown under "What Nimbus remembers about you" after zero saved notes and no connected accounts.
  - Footer claims "Memories are built from your notes and connected accounts."
  - Cause unknown: likely hardcoded placeholder data, possibly another account's data. Severity capped at P2 on that uncertainty.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-power-user/session.log:14`
  > "You prefer to schedule meetings on Tuesday afternoons."
  > "None of that is true."
- **Repro:**
  1. Sign in as a new user, create a workspace, save no notes.
  2. Open "Memories" (`/app/memories.html`).
  3. Observe three statements about the user.
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/memories.html` · build `unknown (not recorded)` · `[04:30]`; also `power-user` `[02:30]`
- **Expected:** An empty state ("Nothing remembered yet") until notes or accounts exist, or only data derived from the user's own content.
- **Actual:** "You prefer to schedule meetings on Tuesday afternoons." · "Your team uses Jira and Slack." · "You are working on a product launch in Q4."
- **Fix:** Replace the hardcoded memories in `memories.html` with an empty state, and render only memories derived from the signed-in user's own notes.

---

## Dropped for want of evidence
- Settings "Federated graph replication" default-on may not match the signup choice (power-user chose Federated graph, novice chose Hybrid mesh) — settings state was not compared per persona.
- Search returning nothing — expected, since no note was ever stored; cannot test search independently.

## For other lenses
- Irreversible "Federated graph / Sovereign vault / Hybrid mesh" choice before the product is seen — ux, onboarding.
- Jargon in Settings ("Enable webhook sync", "Vault attestation") and "Cards"/"New block" naming — content.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux, missing feature.
- Empty dashboard gives no next step; promise "remembers everything" vs. blank start — onboarding.

## Coverage gaps
- Note edit and delete, export, and the settings controls were never exercised.
- Single device profile (desktop-1440x900); no refresh, back-button or two-tab state tests; build id not recorded.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
