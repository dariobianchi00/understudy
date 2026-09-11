# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: console errors, failed requests, dead ends, broken states, lying feedback, state corruption
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (manifest `persona_mode: generic`)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 4f718170ee18 — Save reports success while the note is silently discarded
- **Severity:** P0
- **So what:** Both personas wrote a note, were told it saved, and lost it — the product's core promise (never lose your stuff) fails on the first real write.
- **Framework tags:** Failed requests, Lying feedback
- **Flow:** shape_2
- **Locator:** /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST http://localhost:8765/api/notes → 500 internal error` fires on every save attempt (novice at 03:05 and 03:50; power-user at 01:00)
  - UI shows a green "Saved ✓" toast despite the 500 (screenshot `04-note-saved-toast.png`)
  - Dashboard "Your cards" and search both remain empty for the saved title immediately after ("Nothing here yet.", "No results for 'Dentist'" / "No results for 'Roadmap'")
- **Evidence:** `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-novice/screenshots/04-note-saved-toast.png` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/network-full.txt:3` · `persona-power-user/screenshots/03-search-empty.png`
  > "[POST] http://localhost:8765/api/notes → 500 internal error  (03:05)"
- **Repro:**
  1. Complete signup, land on empty dashboard.
  2. Click "New block", enter a title and body, click Save.
  3. Observe "Saved ✓" toast and redirect to dashboard.
  4. Observe dashboard "Your cards" still reads "Nothing here yet." and searching the title returns no results.
- **Fix:** Make `POST /api/notes` return 200 and persist the note; gate the "Saved ✓" toast on a successful server response instead of firing unconditionally.

### 50b6f9524315 — Memories panel invents personal facts the user never entered
- **Severity:** P0
- **So what:** A workspace with zero saved notes and zero connected accounts is shown confident, specific claims about the user's team, tools and schedule — the exact "confident nonsense about the persona's own data" failure mode.
- **Framework tags:** Lying feedback
- **Flow:** surfaces
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4." (screenshot `06-memories.png`)
  - Neither persona had written more than one note (novice: one dentist note, never persisted) or connected any account before viewing this screen
  - Footer text reads "Memories are built from your notes and connected accounts." — directly contradicted by the empty state of both
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Sign up as a new workspace, do not connect any accounts.
  2. Write zero or one notes.
  3. Navigate to "Memories".
  4. Observe specific claims about meeting preferences, tools and projects with no corresponding user data.
- **Fix:** Remove or clearly label the Memories panel's demo/placeholder content until it is backed by real user data; never render fabricated claims as fact.

### 8a23401280b4 — Uncaught ReferenceError on every dashboard load: `renderGraphOverlay is not defined`
- **Severity:** P3
- **So what:** A broken script fires on every dashboard visit; no visual corruption or blocked interaction was observed, so impact is limited to code health rather than the persona's experience.
- **Framework tags:** Console errors
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - `[error] dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined` recurs on repeated dashboard loads for both personas
  - Dashboard renders correctly regardless (screenshots `02-dashboard-empty.png`, `02-dashboard.png`) — no missing UI or broken layout observed
  - Neither persona mentioned or reacted to this in their debrief or session log
- **Evidence:** `persona-novice/console-full.txt:1` · `persona-novice/console-full.txt:2` · `persona-novice/console-full.txt:4` · `persona-novice/console-full.txt:6` · `persona-power-user/console-full.txt:1` · `persona-power-user/console-full.txt:3`
  > "[error] dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined"
- **Repro:**
  1. Complete signup with any workspace type.
  2. Land on /app/dashboard.html.
  3. Open browser console — error fires immediately, and again on every subsequent dashboard load.
- **Fix:** Define `renderGraphOverlay` (or remove the dead call) so the dashboard script does not throw on load.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Search may be broken independent of the save failure — every search observed in this run targeted a title that failed to save, so no artifact isolates search from the persistence bug.

## For other lenses
- Forced, irreversible workspace-type choice ("Federated graph / Sovereign vault / Hybrid mesh") before the product has shown any value — onboarding/ux lens.
- Jargon in Settings ("Enable webhook sync", "Vault attestation") and unclear relationship between signup choice and "Federated graph replication" toggle — content/ux lens.
- Ambiguous "Cards" vs "New block" vs "notes" terminology across the nav — content lens.
- No keyboard shortcuts despite power-user expectation (Ctrl+K, Ctrl+N, / all no-ops) — ux lens (missing feature, not a defect).

## Coverage gaps
- Neither persona reached a populated notes list, an edit/delete flow, or multi-device/tab behaviour — save never succeeded once in this run.
- Mobile/responsive viewports not tested — both personas ran at desktop 1440×900 only.

## Appendices
- A. Persona debriefs: `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines: `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index: `persona-novice/screenshots/`, `persona-power-user/screenshots/`
