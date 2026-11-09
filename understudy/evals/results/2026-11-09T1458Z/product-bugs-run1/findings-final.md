# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: bug report — console, network, dead ends, broken and lying states
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### abda6b931428 — Save returns 500 but shows "Saved ✓" and the note is lost
- **Severity:** P0
- **So what:** Users believe notes are stored; every note written is silently destroyed, so the core job fails.
- **Framework tags:** lying-feedback, failed-request, data-loss
- **Flow:** write a note and find it again
- **Locator:** POST /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST http://localhost:8765/api/notes` returned 500 on every save (novice 03:05 and 03:50; power-user 01:00).
  - A green "Saved ✓" toast appeared anyway, then the dashboard showed "Nothing here yet."
  - Search for the saved title returned "No results for 'Dentist'."
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/new.html` · build `unknown (not recorded)` · `[03:05]`; also `power-user` · desktop 1440×900 · same URL · `[01:00]`
- **Expected:** A 2xx response, the note persisted, and it appears under "Your cards" and in search. On failure, an error message and the draft kept.
- **Actual:** `new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)`, with a success toast and an empty list.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17-19` · `persona-novice/console-full.txt` · `persona-novice/network-full.txt` · `persona-power-user/session.log:11`
  > "[POST] http://localhost:8765/api/notes → 500 internal error  (03:05)"
  > "It said saved."
- **Repro:**
  1. Sign in, create a workspace, open "New block" (`/app/new.html`).
  2. Enter title "Dentist" and a body, then click Save.
  3. Observe the "Saved ✓" toast and the redirect to the dashboard.
  4. Observe "Nothing here yet."; search "Dentist" returns "No results".
  5. Check the network log for the 500 on `POST /api/notes`.
- **Fix:** Make `POST /api/notes` succeed; show the toast only on a 2xx and show an error with the draft kept otherwise.

### 240581789a43 — Memories page shows three facts the user never supplied
- **Severity:** P1
- **So what:** Fabricated personal claims make users distrust the product, and the "Saved" feedback with it.
- **Framework tags:** wrong-data, lying-feedback
- **Flow:** write a note and find it again
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - The page lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack." and "You are working on a product launch in Q4."
  - Footer reads "Memories are built from your notes and connected accounts." Both accounts had zero saved notes and no connected accounts.
  - Both personas called the content untrue; the novice questioned whether "Saved" was also invented.
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/memories.html` · build `unknown (not recorded)` · `[04:30]`; also `power-user` `[02:30]`
- **Expected:** An empty state, or only facts derived from the user's own notes or connected accounts.
- **Actual:** Three hard-coded-looking statements presented as what "Nimbus remembers about you".
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist."
- **Repro:**
  1. Complete signup with a fresh workspace; save no notes (saves fail anyway).
  2. Click "Memories" in the top nav.
  3. Observe the three statements.
- **Fix:** Render an empty state on `/app/memories.html` until memories derive from real user data; remove the seeded entries.

### fbe00c88e0f1 — Dashboard throws "ReferenceError: renderGraphOverlay is not defined" on every load
- **Severity:** P2
- **So what:** An uncaught exception on the main screen; it may be why the list never renders, though that is unconfirmed.
- **Framework tags:** console-error
- **Flow:** write a note and find it again
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Logged on each dashboard load: 4 times for novice, 2 for power-user.
  - No persona noticed it directly; its link to the empty list is not proven.
- **Environment:** persona `novice` · desktop 1440×900 · `http://localhost:8765/app/dashboard.html` · build `unknown (not recorded)` · `[00:55]`; also `power-user` `[00:30]`
- **Expected:** No uncaught exceptions; `renderGraphOverlay` defined or its call removed.
- **Actual:** `dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined`
- **Evidence:** `persona-novice/console-full.txt` · `persona-power-user/console-full.txt` · `persona-novice/screenshots/02-dashboard-empty.png`
  > "dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined"
- **Repro:**
  1. Sign in and open `/app/dashboard.html`.
  2. Open the browser console.
  3. Observe the ReferenceError. Exact timestamps beyond the first load were not recorded.
- **Fix:** Define or import `renderGraphOverlay` in `dashboard.html`, or guard the call; then retest whether saved notes render.

---

## Dropped for want of evidence
- Search "doesn't work" (power-user 03:00) — no note ever persisted, so search could not be tested; no search request was logged.

## For other lenses
- Workspace type "Federated graph / Sovereign vault / Hybrid mesh", "cannot be changed later", with no explanation — ux/onboarding.
- Cards vs "New block" vocabulary, and Settings jargon ("Vault attestation") — content.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux.
- Empty dashboard gives no next step — onboarding.

## Coverage gaps
- Saved-note list, edit and delete never reached: no note persisted.
- Export to Markdown never exercised.
- Mobile and other viewports not tested; build id not recorded.
- Screenshot `04-note-saved-toast.png` shows the empty form, not the toast; toast cited from session.log.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
