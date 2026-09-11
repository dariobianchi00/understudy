# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: console errors, failed requests, dead ends, broken states, lying feedback, state corruption
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 7eaf39274900 — Save reports success but the note is never persisted
- **Severity:** P0
- **So what:** The user writes real content, is told it is saved, and loses it with no warning — twice, for both personas.
- **Framework tags:** lying feedback, broken state
- **Flow:** shape_2
- **Locator:** /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST http://localhost:8765/api/notes → 500 internal error` fires on every save attempt (novice at 03:05 and 03:50, power-user at 01:00)
  - UI shows a green "Saved ✓" toast immediately after the 500 (screenshot `04-note-saved-toast.png`)
  - Dashboard "Your cards" and search both remain empty/no-results for the same title right after the "success" toast
- **Evidence:** `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-novice/session.log:17` · `persona-novice/screenshots/04-note-saved-toast.png` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/network-full.txt:3` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png`
  > "Saved twice, empty twice. It is lying to me."
- **Repro:**
  1. Sign up, land on empty dashboard.
  2. Click "New block", enter a title and body, click Save.
  3. Observe "Saved ✓" toast while devtools Network shows `POST /api/notes` returning 500.
  4. Return to dashboard or search for the title — nothing is there.
- **Fix:** Make the save button surface the 500 as an error, not a success toast, and fix the endpoint so the write actually persists.

### d477925d4aa6 — Memories panel fabricates personal facts the user never entered
- **Severity:** P0
- **So what:** The product states confident, specific claims about the user's habits and team that are false, before they have entered any real data.
- **Framework tags:** lying feedback
- **Flow:** surfaces
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Memories page reads "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4." for an account with zero successfully-saved notes
  - Page caption claims "Memories are built from your notes and connected accounts" — no notes exist and no accounts were connected
  - Both personas independently identified the claims as false for their session
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
- **Repro:**
  1. Sign up as a fresh account (any workspace type).
  2. Do not connect any accounts; optionally attempt to save a note (see finding 7eaf39274900).
  3. Click "Memories" in the top nav.
  4. Observe three specific personal claims with no basis in any data the account has.
- **Fix:** Remove or clearly label the Memories panel as sample/demo content until it is wired to real user data.

### 20d93d7ac963 — Uncaught ReferenceError fires on every dashboard load
- **Severity:** P3
- **So what:** Indicates a broken script path on the dashboard; no visible UI consequence was observed by either persona this run.
- **Framework tags:** console error
- **Flow:** shape_1
- **Locator:** dashboard.html:renderGraphOverlay
- **Personas hit:** novice, power-user
- **Observed:**
  - `[error] dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined` fires on every dashboard.html load for both personas
  - Recurs 3 times in the novice session (console-full.txt) and 2 times in the power-user session
  - No layout break or missing element was noted by either persona in debrief or reaction log
- **Evidence:** `persona-novice/console-full.txt:1` · `persona-novice/console-full.txt:2` · `persona-novice/console-full.txt:4` · `persona-power-user/console-full.txt:1` · `persona-power-user/console-full.txt:3`
- **Repro:**
  1. Sign up and land on, or navigate back to, `/app/dashboard.html`.
  2. Open devtools console.
  3. Observe `Uncaught ReferenceError: renderGraphOverlay is not defined` on load.
- **Fix:** Define or remove the dead `renderGraphOverlay` call from dashboard.html's load path.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- None dropped this run — all observed defects in session.log/console-full.txt/network-full.txt had a matching screenshot or verbatim log line.

## For other lenses
- Irreversible, unexplained workspace-type choice ("Federated graph / Sovereign vault / Hybrid mesh", cannot be changed later) forced before any product value is shown — onboarding/ux.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) despite power-user expectation of a fast, keyboard-driven tool — ux/onboarding.
- "Cards" vs "New block" vs "notes" terminology inconsistency confuses navigation — content/ux.
- Settings label "Federated graph replication" duplicates the signup workspace-type wording with no link or explanation of whether it's the same setting — ux/content.
- Jargon in Settings ("Enable webhook sync", "Vault attestation") with no explanation — content/ux.

## Coverage gaps
- Cards list view never populated (save never succeeded), so its layout/behavior with real data is untested.
- No refresh or second-tab test performed — state-corruption checks (back button, two tabs) not exercised this run.
- No mobile/responsive viewport tested — both personas ran desktop-1440x900 only.

## Appendices
- A. Persona debriefs: `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines: `persona-novice/session.log`, `persona-novice/timeline.json`, `persona-power-user/session.log`, `persona-power-user/timeline.json`
- C. Screenshot index: `persona-novice/screenshots/`, `persona-power-user/screenshots/`
