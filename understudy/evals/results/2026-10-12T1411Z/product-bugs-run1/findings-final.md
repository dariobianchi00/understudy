# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: bug report — console, network, dead ends, broken states, lying feedback, state corruption
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Build id: not recorded in the run folder

---

## Findings

### 337d03fee7ba — Saving a note fails with HTTP 500 but the UI shows "Saved ✓" and the note is lost
- **Severity:** P0
- **So what:** Users believe notes are stored, then lose them; 3 of 3 save attempts lost data and both personas quit.
- **Framework tags:** lying-feedback, failed-request, data-loss
- **Flow:** write-and-find-a-note
- **Locator:** POST /api/notes
- **Personas hit:** novice, power-user
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/new.html` · build unknown · `[03:05]` and `[03:50]`; persona `power-user` · desktop-1440x900 · same URL · `[01:00]`
- **Expected:** Save returns 2xx, note appears under "Your cards" and is findable by search; the toast appears only on success.
- **Actual:** `[POST] http://localhost:8765/api/notes → 500 internal error`; the UI still shows green "Saved ✓" and redirects to the dashboard showing "Nothing here yet." Search for "Dentist" returns "No results for 'Dentist'."
- **Observed:**
  - 3 saves (novice ×2, power-user ×1) all returned 500; zero notes ever listed or searchable.
  - Success toast and redirect appeared regardless of the 500.
  - Screenshot 04 shows the empty form, not the toast; the toast rests on the session log only.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/screenshots/04-note-saved-toast.png` · `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-novice/console-full.txt:3` · `persona-power-user/session.log:11` · `persona-power-user/network-full.txt:3`
  > "new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)"
  > "It said saved." / "Save doesn't save and search doesn't search."
- **Repro:**
  1. Complete signup (any workspace type) and open `/app/new.html` via "New block".
  2. Enter Title "Dentist" and a few lines of body.
  3. Click Save; observe "Saved ✓" and POST /api/notes → 500 in the network log.
  4. On the dashboard, observe "Nothing here yet."; search "Dentist" returns no results.
- **Fix:** Fix the 500 in the /api/notes handler, and show "Saved ✓" only on a 2xx response, with an error toast and the draft retained otherwise.

### 2fdad883534a — Memories shows three facts the user never supplied, on an account with zero notes
- **Severity:** P1
- **So what:** Invented personal claims, shown as the user's own, made the novice doubt even the save confirmation.
- **Framework tags:** broken-state, wrong-data
- **Flow:** memories
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/memories.html` · build unknown · `[04:30]`; persona `power-user` · desktop-1440x900 · same URL · `[02:30]`
- **Expected:** With no stored notes or connected accounts, Memories shows an empty state.
- **Actual:** Heading "What Nimbus remembers about you" lists three items and a footer claiming they come from the user's own notes.
- **Observed:**
  - Items: "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer: "Memories are built from your notes and connected accounts." Zero notes were saved and no accounts were connected.
  - Source of the data is unknown: placeholder, another account, or generated content. Not determinable from the logs.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist."
- **Repro:**
  1. Sign up a new workspace; do not save any notes (saving fails anyway).
  2. Click "Memories" in the top menu.
  3. Observe the three statements above.
  4. Source of the data could not be traced from the run folder.
- **Fix:** Render an empty state when no notes exist, and remove hard-coded or cross-account demo memories from /app/memories.html.

### 11c644c9bb69 — Dashboard throws Uncaught ReferenceError: renderGraphOverlay is not defined on every load
- **Severity:** P2
- **So what:** An undefined function in the dashboard script may be breaking card rendering; it fired 6 times across 2 sessions.
- **Framework tags:** console-error
- **Flow:** dashboard
- **Locator:** dashboard.html
- **Personas hit:** novice, power-user
- **Environment:** persona `novice` · desktop-1440x900 · `http://localhost:8765/app/dashboard.html` · build unknown · timestamp not recorded in console-full.txt; persona `power-user` · desktop-1440x900 · same URL · timestamp not recorded
- **Expected:** Dashboard loads without script errors.
- **Actual:** `Uncaught ReferenceError: renderGraphOverlay is not defined` on each dashboard load.
- **Observed:**
  - 4 occurrences in the novice log plus 2 in the power-user log.
  - Visible effect unconfirmed: the dashboard was empty, but no note was ever stored, so the error is not shown to be the cause.
  - Likely tied to the "Federated graph" workspace feature; not verified.
- **Evidence:** `persona-novice/console-full.txt:1` · `persona-novice/console-full.txt:4` · `persona-novice/console-full.txt:6` · `persona-power-user/console-full.txt:1` · `persona-power-user/console-full.txt:3`
  > "dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined"
- **Repro:**
  1. Complete signup and land on `/app/dashboard.html`.
  2. Open the browser console.
  3. Observe the ReferenceError; it recurs on each return to the dashboard.
- **Fix:** Define or import `renderGraphOverlay` in dashboard.html, or guard the call, then confirm cards render once saving works.

---

## Dropped for want of evidence
- Search returning nothing for saved notes as a separate bug — no search request in network logs; it follows from finding 337d03fee7ba.

## For other lenses
- Workspace-type choice ("Federated graph / Sovereign vault / Hybrid mesh", "This cannot be changed later.") is jargon before first value — onboarding/content.
- "Cards" vs "New block" naming mismatch — content.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux.
- Settings jargon ("Vault attestation", "Enable webhook sync") — content.

## Coverage gaps
- Note edit/delete, Markdown export and the settings toggles were never exercised.
- Only desktop-1440x900 tested; no mobile profile.
- Console logs carry no timestamps.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
