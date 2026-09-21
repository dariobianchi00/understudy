# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: console/network evidence first, correlated with persona reaction and debrief
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 2b77595fb927 — Save reports success while the note is never persisted
- **Severity:** P0
- **So what:** Both personas believe their work is saved and walk away; the note does not exist anywhere, and neither persona had any indication their data was lost until they went looking for it.
- **Framework tags:** Lying feedback, Failed request, Broken state
- **Flow:** shape_2
- **Locator:** /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST http://localhost:8765/api/notes` returns `500 (Internal Server Error)` on every save attempt, for both personas, in both console and network logs.
  - The UI shows a green "Saved ✓" toast regardless of the 500, then routes back to a dashboard that still reads "Nothing here yet."
  - Searching for the note's exact title immediately afterward returns "No results for '<title>'" — the note was never written.
- **Evidence:** `persona-novice/screenshots/04-note-saved-toast.png` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/console-full.txt` (`[error] new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)`) · `persona-novice/network-full.txt:5` and `:7` · `persona-novice/session.log:17-20` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/console-full.txt` (`[error] new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)`) · `persona-power-user/network-full.txt:3` · `persona-power-user/session.log:11`
  > "Saved twice, empty twice. It is lying to me." — novice, session.log:20
  > "Save doesn't save and search doesn't search. Nothing else matters until those work." — power-user, session.log:15
- **Repro:**
  1. Create a workspace (any of the three types) and land on the empty dashboard.
  2. Click "New block", enter a title and body, click Save.
  3. Observe the "Saved ✓" toast appear and the app return to the dashboard.
  4. Check Network tab: `POST /api/notes` returned `500`.
  5. Dashboard still shows "Nothing here yet."; searching the note's title returns no results.
- **Fix:** Gate the "Saved ✓" toast on a 2xx response from `/api/notes`; on failure, show an error and keep the user's draft in the form instead of navigating away.

---

### 07f1a46a1363 — Memories panel invents personal facts with no underlying data
- **Severity:** P0
- **So what:** The panel states it is "built from your notes and connected accounts," but shows the same three specific claims to an account with zero notes and zero integrations — a persona cannot tell real personalization from filler, and it retroactively undermines trust in every other signal the product gives (including the save toast).
- **Framework tags:** Lying feedback, Broken state
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Memories page reads "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4." for an account with zero saved notes and no connected accounts.
  - Caption under the claims: "Memories are built from your notes and connected accounts."
  - Both personas explicitly rejected the claims as false and generalized distrust to the rest of the product.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-power-user/session.log:14` · `persona-power-user/timeline.json` (reaction: "Memories aren't mine. A demo panel, I assume.")
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?" — novice, session.log:22
  > "Not me. Whatever — a demo panel, I assume. Not going to trust it." — power-user, session.log:14
- **Repro:**
  1. Create a fresh workspace with zero notes and no connected integrations.
  2. Navigate to Memories from the top nav.
  3. Observe three specific personal claims displayed under a caption that says they are derived from the user's own notes and accounts.
- **Fix:** Either compute Memories from actual note content/connected accounts, or replace the fabricated claims with an honest empty state ("Nothing to show yet") until real data exists.

---

### 2b5127b7eee6 — Uncaught ReferenceError `renderGraphOverlay is not defined` on every dashboard load
- **Severity:** P3
- **So what:** No persona noticed a visual break, but the error fires on 100% of dashboard loads for both workspace types, indicating a feature (graph overlay) that has never worked.
- **Framework tags:** Console error
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - `dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined` logged on every dashboard visit for both personas (3 occurrences for novice, 2 for power-user).
  - Occurs regardless of which workspace type was chosen at signup (novice picked Hybrid mesh, power-user picked Federated graph).
  - No visible layout break in the corresponding screenshots — the dashboard renders "Your cards / Nothing here yet." normally.
- **Evidence:** `persona-novice/console-full.txt:1-6` (`[error] dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined`) · `persona-power-user/console-full.txt:1,3` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-power-user/screenshots/02-dashboard.png`
- **Repro:**
  1. Sign up and land on `/app/dashboard.html` with any workspace type.
  2. Open the browser console.
  3. Observe `Uncaught ReferenceError: renderGraphOverlay is not defined` on load, repeated on every subsequent dashboard visit.
- **Fix:** Define `renderGraphOverlay` or remove the dead call site from `dashboard.html`.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Search may fail even for successfully-saved notes — not observed, since no note was ever persisted this run to test search against real data.

## For other lenses
- Forced, irreversible workspace-type choice ("Federated graph / Sovereign vault / Hybrid mesh") before the product has shown any value — onboarding/UX.
- Jargon in Settings ("Enable webhook sync", "Federated graph replication", "Vault attestation") with no explanation — content/UX.
- "Cards" vs "blocks" vs "notes" naming inconsistency in nav and copy — content.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, `/`) for a power-user persona who expected them — UX.
- "Federated graph replication" setting duplicates workspace-type language with no link back — content/UX.

## Coverage gaps
- Mobile/narrow viewport never tested — both personas ran at 1440×900 desktop.
- No persona attempted edit or delete of an existing note (impossible — no note ever persisted).
- Export ("Markdown, all cards") button was seen but never clicked by either persona.

## Appendices
- A. Persona debriefs: `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines: `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index: `persona-novice/screenshots/`, `persona-power-user/screenshots/`
