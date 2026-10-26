# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: first-value funnel (`first-value.md`) · Layer C tags (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT) · severity rubric
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on invented personas
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached signup (after auth wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen | ✓ 00:48 (guessed "Hybrid mesh") | ✓ <00:30 ("Federated graph") |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| First note written, Save clicked | ✓ 03:05 | ✓ 01:00 |
| Note persisted and findable | ✗ 500 twice (03:05, 03:50) | ✗ 500 (01:00) |
| **First value reached** | ✗ | ✗ |
| Returned to a second task | — abandoned 06:30 | — abandoned 03:00 |

**Steps to value (required path):** 5 — pick workspace type · Create workspace · New block · write · Save · **Time to value:** not reached (0 of 2) · **Drop-off:** Save → dashboard, `/app/new.html` POST `/api/notes` → 500

- Both drop-offs are **abandonment, not time-out**: 06:30 and 03:00 of a 90-minute cap.
- Novice: "I've spent six minutes and I have zero notes saved … I'd stop here." (`persona-novice/session.log:25`)
- Power-user: "Enough. Save doesn't save and search doesn't search." (`persona-power-user/session.log:15`)
- `timeline.json` records novice first value at 161 s (02:41): the live word-count/preview. Not first value — nothing survived Save; the persona's own objective is `gave_up: true`.
- Wandering beyond the required path: novice searched an empty workspace, re-wrote the note, probed Memories and Settings (2 hunts); power-user tried Ctrl+K / Ctrl+N / `/` (1 hunt).

---

## Findings

### 6b7e0f910214 — Save confirms success while the server rejects the note, so no persona ever kept a note
- **Severity:** P0
- **So what:** 2 of 2 personas reached the one action that delivers value, were told it worked, and left with nothing.
- **Framework tags:** C-TTFV, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows green "Saved ✓"; network logs `POST /api/notes → 500` each time (3 attempts across both personas).
  - Dashboard returns to "Nothing here yet."; search for the note title returns "No results".
  - Both personas abandoned within minutes; debrief Q3 for both: "No. Nothing."
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-novice/network-full.txt:5` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/network-full.txt:3`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
- **Repro:**
  1. Complete signup, open "New block".
  2. Enter a title and body, click Save.
  3. Observe "Saved ✓" toast; watch `POST /api/notes` return 500; dashboard still "Nothing here yet."
- **Fix:** Fix the `/api/notes` 500, and show "Saved ✓" only after a 2xx — otherwise show an error with Retry and keep the draft.

### b18d9d48c2f8 — Memories page asserts invented facts about a brand-new user, collapsing trust in every other confirmation
- **Severity:** P1
- **So what:** It turned a failed save into suspected fabrication — the novice concluded the product invents things, including "Saved".
- **Framework tags:** C-ABANDON, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice, power-user
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Neither persona had connected an account or saved a note; footer says "Memories are built from your notes and connected accounts."
  - Both debriefs cite it on Q4 promise match: "claims things I didn't" / "aren't mine".
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:22` · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Sign up a fresh workspace; save nothing, connect nothing.
  2. Open Memories.
  3. Observe three specific claims about the user.
- **Fix:** Show an empty state on Memories for new workspaces ("Nimbus will learn from your notes as you write") and never ship seeded memories to real accounts.

### 5d2f19bb19ee — Empty dashboard offers no next step, contradicting the never-start-from-zero promise
- **Severity:** P2
- **So what:** The novice arrived expecting her stuff, got "Nothing here yet." with no prompt, and spent 45 s searching an empty workspace.
- **Framework tags:** C-STEPS, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" shows only "Nothing here yet." — no create button, no import, no example.
  - Novice searched "meeting" at 01:20 before finding "New block" at 01:40.
  - Power-user expected an empty start and was unaffected.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13`
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a new workspace.
  2. Land on `/app/dashboard.html`.
  3. Observe the empty "Your cards" panel with no call to action.
- **Fix:** Replace "Nothing here yet." with a "Write your first note" button and an import option that delivers on "never start from zero".

### 12b1253dbc32-a — Irreversible workspace-type choice is demanded before the novice has seen the product
- **Severity:** P2
- **So what:** First screen forces a permanent guess the novice could not understand — 43 s of hesitation and an uninformed choice.
- **Framework tags:** C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh" — no descriptions.
  - "This cannot be changed later." beneath the options.
  - Novice deliberated 00:05–00:48 and picked by guess; continued.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the auth wall; land on `/app/signup.html`.
  2. Observe three unexplained options and "This cannot be changed later."
- **Fix:** Default the workspace type silently, or move it to Settings with a one-line plain-English description of each and make it changeable.

### fef3e5530b55-b — Workspace-type choice cannot be traced to the matching Settings toggle afterwards
- **Severity:** P3
- **So what:** The power-user accepted the step but could not tell whether his signup choice and the Settings toggle were the same thing.
- **Framework tags:** C-SOWHAT
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Power-user picked "Federated graph" at signup without complaint ("Fine — I've seen worse").
  - Settings shows "Federated graph replication" checked, no link back to the signup choice.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:8` · `persona-power-user/session.log:13`
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Pick "Federated graph" at signup.
  2. Open Settings; observe "Federated graph replication" checked with no explanation.
- **Fix:** Label the Settings row "Workspace type: Federated graph (chosen at signup)" with a short description.

### 60a164192fd9 — Nav labels Cards and New block never say note, costing the novice a hunt to start writing
- **Severity:** P2
- **So what:** The novice came to write a note and had to guess that "New block" was how; one of her 2 recorded hunts.
- **Framework tags:** C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html#nav
- **Personas hit:** novice
- **Observed:**
  - Top nav reads "Cards", "New block", "Memories", "Settings"; search placeholder says "Search your notes".
  - Three nouns for one object: card, block, note.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:14` · `persona-novice/timeline.json`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing? Clicked "New block"."
- **Repro:**
  1. Land on the dashboard.
  2. Look for a way to write a note; compare nav labels with the search placeholder.
- **Fix:** Rename "New block" to "New note" and "Cards" to "Notes" across nav, dashboard heading and Export label.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast itself — `persona-novice/screenshots/04-note-saved-toast.png` actually shows an empty "New block" form, no toast; toast rests on `session.log:17` only.
- Power-user Ctrl+K / Ctrl+N / `/` producing nothing — log line only, no screenshot; also a ux matter.

## For other lenses
- `POST /api/notes → 500` and `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load — bugs.
- No keyboard shortcuts for a keyboard-first evaluator (`persona-power-user/session.log:12`) — ux.
- Settings jargon: "Enable webhook sync", "Vault attestation" (`persona-novice/screenshots/07-settings.png`) — content.
- Memories copy "What Nimbus remembers about you" over seeded data — content.

## Coverage gaps
- No persona reached a saved note, so search-returns-note (objective criterion) was never testable.
- Export ("Markdown, all cards") was seen, never clicked.
- Desktop 1440×900 only; no mobile.
- Marketing page carrying the "remembers everything" promise was not captured.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 01 signup type · 02 empty dashboard · 03 new block · 04 (mislabelled, empty form) · 05 empty dashboard after save · 06 memories · 07 settings; power-user: 02 dashboard · 03 empty after search · 07 settings
