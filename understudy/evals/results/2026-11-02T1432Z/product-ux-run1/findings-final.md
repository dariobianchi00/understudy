# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10) · Layer B (HAX — applies: "Memories" is a user-facing inferred-profile surface) · Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user; both desktop-1440x900)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 6870a830c545 — Save confirms success with a toast while the note is never stored, listed or searchable
- **Severity:** P0
- **So what:** Both personas lost every note they wrote, gave up, and said they would not keep using or pay for it.
- **Framework tags:** A1, A9, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows "Saved ✓", then returns to a dashboard still reading "Nothing here yet." — novice twice (03:05, 03:50), power-user once (01:00).
  - Searching the exact title returns "No results for 'Dentist'" / no results for "Roadmap".
  - Both objectives marked `gave_up: true`; network shows `POST /api/notes → 500` at each save (cited as cause only — the error belongs to bugs).
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/timeline.json` objectives[0].gave_up · `persona-novice/network-full.txt` `[POST] /api/notes → 500`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me." (novice)
  > "Save doesn't save and search doesn't search. Nothing else matters until those work." (power-user)
- **Repro:**
  1. Sign up and open "New block".
  2. Enter a title and body, click Save.
  3. Observe "Saved ✓", then an empty "Your cards" list; search the title — no results.
- **Fix:** Show "Saved ✓" only after the server confirms the write; on failure keep the draft on screen with a plain-language error and a Retry button.

### d8e84586fd20 — Memories page states fabricated facts about a brand-new user, collapsing the novice's trust in Save too
- **Severity:** P0
- **So what:** Invented facts about her own life made the novice doubt every other claim the product makes, including "Saved".
- **Framework tags:** B-G1, B-G2, B-G11, A2, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — she had zero saved notes and no connected accounts.
  - She stopped 1:40 later, citing this page; debrief Q4 names it.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Sign up a fresh workspace; connect nothing.
  2. Open Memories.
  3. Observe three specific personal claims with no source.
- **Fix:** Show an honest empty state on Memories until real notes exist, and link each memory to the note or account it came from.
- Torn P0/P1: rubric names "confident nonsense about the persona's own data" as P0, and her distrust spread to the core Save flow.

### 6934f38b556a — Memories page shows facts the power-user never gave, so he dismisses the feature as a demo
- **Severity:** P1
- **So what:** The evaluator wrote off the product's headline "remembers everything" feature and named it in his reasons not to switch.
- **Framework tags:** B-G1, B-G11, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Read "Tuesday meetings, Jira, Q4 launch" and concluded "Not me."
  - Assumed it was a demo panel; explicitly declined to trust it.
  - Debrief: product "claims things I didn't."
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` Q4 · `persona-novice/screenshots/06-memories.png` (same screen; power-user did not capture it)
  > "Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Sign up a fresh workspace.
  2. Open Memories.
  3. Observe facts unrelated to anything entered.
- **Fix:** Label any sample content as "Example" or remove it; show memories only when traceable to the user's own notes.

### 78909f81f063 — Signup forces an irreversible workspace-type choice in unexplained jargon before any product is shown
- **Severity:** P2
- **So what:** The novice guessed blind on a permanent decision 20 seconds in; a more cautious user leaves here.
- **Framework tags:** A2, A3, A5, A10, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Options "Federated graph", "Sovereign vault", "Hybrid mesh" with no descriptions; note "This cannot be changed later."
  - Novice hesitated 43s (00:05–00:48), picked "Hybrid mesh" because "it sounds like it includes the other two".
  - Power-user shrugged it off ("Fine — I've seen worse") — severity flip, see exec summary.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall on a fresh account.
  2. Land on "Before we begin, choose your workspace type".
  3. Observe three unexplained options and "This cannot be changed later."
- **Fix:** Default the workspace type silently and move it to Settings, or add a one-line plain-English description and make it changeable.

### cc890adf9a61 — Empty dashboard says only Nothing here yet and offers no first action
- **Severity:** P2
- **So what:** The novice arrived expecting her stuff, found a blank page, and had to hunt for how to start.
- **Framework tags:** A6, A10, C-TTFV, C-SOWHAT
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel reads only "Nothing here yet." — no button, hint or sample.
  - Novice tried search first (01:20), then the menu; reached the editor at 01:55, 60s after landing.
  - Debrief contrasts this with the promise: "it started completely empty".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14` · `persona-novice/persona-debrief.md` Q4
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a new workspace.
  2. Land on the dashboard.
  3. Observe "Nothing here yet." with no call to action.
- **Fix:** Put a "Write your first note" button inside the empty "Your cards" panel, with one line on what Nimbus will do with it.

### e9fae6b6ed5f — One screen calls the same object a card, a block and a note
- **Severity:** P2
- **So what:** The novice could not tell whether "New block" would create one of "Your cards" before clicking.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Nav reads "Cards", "New block"; panel "Your cards"; search placeholder "Search your notes".
  - Novice paused on the menu and asked if they were the same, then clicked "New block".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` t=01:40
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Open the dashboard.
  2. Compare the nav, the panel heading and the search placeholder.
- **Fix:** Pick one noun ("note") and use it in the nav, the editor heading, the list heading and the search placeholder.

### 8c8b44206a36 — Settings reuses the signup term Federated graph with no explanation or link between the two
- **Severity:** P2
- **So what:** Neither persona could tell what the checked-by-default options do or whether they undo the "permanent" signup choice.
- **Framework tags:** A2, A4, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Options "Enable webhook sync", "Federated graph replication" (checked by default), "Vault attestation" — no descriptions.
  - Power-user asked if replication is the signup choice; novice: "No idea".
  - Both found "Export — Markdown, all cards" clear and named it in debrief.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:13` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23`
  > "\"Federated graph replication\" is on by default. I picked that at signup — is this the same thing?"
- **Repro:**
  1. Sign up choosing "Federated graph".
  2. Open Settings.
  3. Observe "Federated graph replication" checked, with no explanation.
- **Fix:** Add a one-line description under each Settings option and state which signup workspace type it relates to.

### 9e4afbd0afb4 — No keyboard shortcuts exist for creating a note or jumping to search
- **Severity:** P2
- **So what:** The power-user, evaluating for a team, expected keyboard-driven capture and found none.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - Tried Ctrl+K, Ctrl+N and / — nothing happened.
  - Pre-session expectation was "fast capture, good search, keyboard-driven".
- **Evidence:** `persona-power-user/session.log:3` · `persona-power-user/session.log:12` · `persona-power-user/findings-raw.json` t=01:30
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Open the dashboard.
  2. Press Ctrl+K, Ctrl+N, or /.
  3. Observe no response.
- **Fix:** Bind / to focus search and Ctrl+N to "New block", and list both in the nav tooltips.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast is not visible in `persona-novice/screenshots/04-note-saved-toast.png` (it shows a blank form) — toast cited from `session.log:17` only.
- Settings and signup checkboxes/radios sit centred, far from their left-aligned labels — visible in screenshots, but no persona reacted to it.
- Live word count and preview were the novice's one moment of value (02:41) — positive, not a finding; preview not visible in the captured screenshot.

## For other lenses
- `POST /api/notes → 500` on every save, and `Uncaught ReferenceError: renderGraphOverlay is not defined` on dashboard — bugs.
- Marketing promise "remembers everything so you never start from zero" vs empty first run — onboarding.
- Jargon density in signup and Settings ("Sovereign vault", "Vault attestation") — content.
- WCAG/accessibility (detached labels) — no lens covers it yet.

## Coverage gaps
- Export was seen but never clicked by either persona.
- Cards nav link never opened separately from the dashboard.
- Power-user did not screenshot Memories; mobile never tested.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index — novice 00–07 (login 00-start excluded), power-user 00, 02, 03, 07
