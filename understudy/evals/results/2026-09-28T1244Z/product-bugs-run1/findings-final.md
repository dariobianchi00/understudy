# Nimbus Notes — bugs findings — Run 2026-09-08 (fixture02)

## Method
- Framework: console/network evidence first, correlated with persona reaction and debrief impact
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (persona_mode: generic; not researched personas)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### f9c10ccd211c — Save reports success while POST /api/notes fails with 500 and the note is never stored
- **Severity:** P0
- **So what:** Both personas wrote a note, got a success confirmation, and never saw it again — the one objective they were sent to complete fails 100% of the time.
- **Framework tags:** Lying feedback, Broken state, Dead end
- **Flow:** shape_2
- **Locator:** /api/notes
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice: clicked Save twice (00:03:05 and 00:03:50), saw "Saved ✓" both times, dashboard read "Nothing here yet." both times, search for the note's title returned no results.
  - Power-user: clicked Save once (00:01:00), saw "Saved ✓", dashboard and search for "Roadmap" both came back empty; concluded "Save doesn't save and search doesn't search" and stopped testing further.
  - Network layer shows the save request actually failing (500) at the same timestamps the UI displayed the success toast.
- **Evidence:** `persona-novice/session.log:17-20` · `persona-novice/network-full.txt:5,7` · `persona-novice/console-full.txt:3,5` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11,15` · `persona-power-user/network-full.txt:3` · `persona-power-user/console-full.txt:2` · `persona-power-user/screenshots/03-search-empty.png`
  > "[error] new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)"
  > "[POST] http://localhost:8765/api/notes → 500 internal error  (03:05)"
  > "Saved twice, empty twice. It is lying to me." — novice, session.log:20
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work." — power-user, session.log:15
- **Repro:**
  1. Sign up, land on empty dashboard.
  2. Click "New block", enter a Title and Body, click Save.
  3. Observe "Saved ✓" toast, then navigate to the dashboard.
  4. Dashboard "Your cards" still reads "Nothing here yet."; searching the note's title in the search box returns "No results".
  5. Network tab / console confirms `POST /api/notes` returned `500 (Internal Server Error)` at the moment Save was clicked.
- **Fix:** Make the Save button surface the real request result — block the "Saved ✓" toast on a non-2xx response and show an error instead; then fix the 500 on `POST /api/notes` so notes actually persist.

### 2b5127b7eee6 — Uncaught ReferenceError: renderGraphOverlay is not defined on every dashboard load
- **Severity:** P3
- **So what:** A dead function reference fires on every dashboard render; no persona noticed or was blocked by it this run, but it indicates unshipped/broken JS on a core page.
- **Framework tags:** Console error
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Fires on every dashboard.html load: 4 times across the novice session (initial load + after each of 2 failed saves + settings-adjacent reload), 2 times for power-user.
  - No visible rendering breakage in the corresponding screenshots — dashboard chrome and "Nothing here yet." empty state render normally.
  - Neither persona mentioned any dashboard visual defect in session.log or debrief.
- **Evidence:** `persona-novice/console-full.txt:1,2,4,6` · `persona-power-user/console-full.txt:1,3` · `persona-novice/screenshots/02-dashboard-empty.png`
  > "[error] dashboard.html:1 Uncaught ReferenceError: renderGraphOverlay is not defined"
- **Repro:**
  1. Complete signup and land on /app/dashboard.html.
  2. Open the browser console.
  3. Observe `Uncaught ReferenceError: renderGraphOverlay is not defined` on load, repeating on every subsequent dashboard render.
- **Fix:** Define `renderGraphOverlay` or remove the call site; add a build/lint check that catches undefined references before deploy.

### 151eda485577 — Memories panel fabricates personal facts and deepens the novice's distrust of the save toast
- **Severity:** P1
- **So what:** The novice explicitly connects the fabricated Memories content to doubting whether "Saved ✓" is also a lie — one broken surface poisons trust in another.
- **Framework tags:** Lying feedback, Broken state
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Memories page shows "What Nimbus remembers about you" with three specific claims ("Tuesday afternoons", "Jira and Slack", "product launch in Q4") for an account that has written exactly one (failed) note about a dentist appointment.
  - Page footer states "Memories are built from your notes and connected accounts" — a claim contradicted by the account having zero connected accounts and zero successfully stored notes.
  - Novice reaction ties this directly to distrust of the save flow, not treated as an isolated issue.
- **Evidence:** `persona-novice/session.log:21-22` · `persona-novice/screenshots/06-memories.png` · `persona-novice/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?" — session.log:22
  > "it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine." — persona-debrief.md, Q4
- **Repro:**
  1. Sign up a brand-new account and do not successfully save any notes (save is broken — see f9c10ccd211c).
  2. Click "Memories" in the top nav.
  3. Observe three specific personal claims and the "built from your notes and connected accounts" tagline, despite no notes or accounts existing.
- **Fix:** Replace the fabricated content with an honest empty state ("No memories yet — write a few notes first") until real extraction from stored notes is implemented.

### f1d1125965d9 — Memories panel fabricates personal facts the power-user writes off as a demo panel
- **Severity:** P2
- **So what:** Erodes trust without stopping the session this run — the power-user shrugged and moved on, but still named it as a broken promise in debrief.
- **Framework tags:** Lying feedback
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Power-user opens Memories after signup, sees the same three fabricated claims, assumes it is placeholder/demo content, and continues to Settings without further investigation.
  - Debrief nonetheless names it directly when asked whether the product matched its promise.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md`
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it." — session.log:14
  > "It remembers nothing I gave it and claims things I didn't." — persona-debrief.md, Q4
- **Repro:**
  1. Sign up a brand-new account.
  2. Click "Memories" in the top nav before writing any notes.
  3. Observe fabricated personal claims with no supporting data.
- **Fix:** Same as f1: replace fabricated content with an honest empty state gated on real note count.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether `04-note-saved-toast.png` actually shows the "Saved ✓" toast — the captured image is visually identical to the pristine, empty "New block" form and does not itself confirm the toast's appearance or text. Not used as evidence for f9c10ccd211c; the claim is instead supported by session.log, network-full.txt and console-full.txt at matching timestamps.

## For other lenses
- "Cards", "blocks", and "notes" used interchangeably in nav and copy; novice couldn't tell if they were the same thing (session.log:14) — content lens.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) despite power-user expecting them (session.log:12, power-user) — UX lens.
- Workspace type choice at signup ("Federated graph / Sovereign vault / Hybrid mesh") is irreversible and unexplained before the user has seen the product — onboarding lens.
- Settings page jargon ("Enable webhook sync", "Federated graph replication", "Vault attestation") with no explanation — content lens.
- Power-user unsure if "Federated graph replication" in Settings is the same choice made at signup, no link between the two (session.log:13) — UX lens.

## Coverage gaps
- Only 2 personas, both desktop 1440×900 — no mobile/tablet viewport tested.
- No persona reached a populated Cards list, note editing, or note deletion — save never succeeded.
- Only one save attempt path exercised (New block form); no autosave, offline, or multi-tab behavior tested.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index — `persona-novice/screenshots/`, `persona-power-user/screenshots/`
