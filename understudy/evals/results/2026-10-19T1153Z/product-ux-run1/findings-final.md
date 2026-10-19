# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10) · Layer B (HAX — applies to the "Memories" surface only) · Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Layer B scope: the only AI-style surface is "What Nimbus remembers about you"; no other screen is tagged B

---

## Findings

### a9e91d5982b3 — Save shows "Saved ✓" but the note never appears in cards or search
- **Severity:** P0
- **So what:** Both personas wrote a note, were told it saved, could not find it, and quit — the product's one job fails silently.
- **Framework tags:** A1, A9, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice saved "Dentist" twice (03:05, 03:50); "Saved ✓" each time; dashboard still "Nothing here yet."; search "No results for 'Dentist'."
  - Power-user saved "Roadmap" at 01:00; "Saved ✓"; dashboard empty; search for "Roadmap" returned nothing.
  - Both marked the objective `gave_up: true`; screenshot 04 captured the blank form, not the toast — toast rests on session.log.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/screenshots/04-note-saved-toast.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-novice/timeline.json` objectives[0].gave_up
  > "Saved twice, empty twice. It is lying to me." — novice
  > "Save doesn't save and search doesn't search. Nothing else matters until those work." — power-user
- **Repro:**
  1. Create a workspace, open "New block".
  2. Enter a title and body, click Save.
  3. Observe "Saved ✓", then the dashboard showing "Nothing here yet."; search the title — "No results".
- **Fix:** Show "Saved ✓" only after the server confirms; on failure keep the draft on screen with a plain error and a Retry button.

### fbc296f43109 — Memories page asserts invented facts about the novice, and she stops trusting "Saved"
- **Severity:** P0
- **So what:** Confident claims about her life she never made spread distrust to the whole product, including the save confirmation.
- **Framework tags:** B-G2, B-G11, A1, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Page titled "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — she had no saved notes and connected nothing.
  - She linked it to the save failure and said she would stop at 06:30.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
  > "the "memories" it does have aren't mine." — debrief Q4
- **Repro:**
  1. Create a fresh workspace; connect no accounts.
  2. Open "Memories".
  3. Observe three specific personal claims with no source.
- **Fix:** Show an empty state on Memories until real notes exist, and link each memory to the note or account it came from.
- **Severity note:** torn P0/P1; P0 because the rubric names "confident nonsense about the persona's own data", and it broke trust in "Saved".

### 41aba06fd452 — Memories page asserts facts the power user never gave, and he writes the panel off
- **Severity:** P1
- **So what:** The headline "remembers everything" feature is dismissed as fake by the evaluator deciding whether to switch his team.
- **Framework tags:** B-G2, B-G11
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Saw the same three claims (Tuesday meetings, Jira, Q4 launch).
  - Rationalised it as a demo panel and stated he would not trust it.
  - Debrief Q4 cites it against the promise.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` (t 02:30) · `persona-power-user/persona-debrief.md` Q4 · `persona-novice/screenshots/06-memories.png` (same page, novice capture)
  > "Not me. Whatever — a demo panel, I assume. Not going to trust it."
  > "It remembers nothing I gave it and claims things I didn't." — debrief Q4
- **Repro:**
  1. Create a fresh workspace.
  2. Open "Memories".
  3. Observe claims unrelated to anything entered.
- **Fix:** Same as the novice variant: empty state until real data exists, plus a visible source link on every memory.

### 81deaedfc658 — Signup forces an irreversible workspace choice between three unexplained terms
- **Severity:** P2
- **So what:** The first decision is a guess the user cannot undo, made before seeing any product — a less patient novice leaves here.
- **Framework tags:** A2, A3, A5, A10
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Options "Federated graph", "Sovereign vault", "Hybrid mesh", no descriptions, warning "This cannot be changed later."
  - Novice spent 43 s (00:05–00:48) and picked "Hybrid mesh" by guessing.
  - Power-user picked in under 30 s with no complaint — non-issue for him (severity flip).
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall.
  2. Land on "Before we begin, choose your workspace type".
  3. Observe three labels with no explanation and "This cannot be changed later."
- **Fix:** Default the workspace type silently, or add one plain sentence per option and make it changeable in Settings.

### 522634e8c888 — Empty dashboard says "Nothing here yet." with no next step toward a first note
- **Severity:** P2
- **So what:** The novice expected her stuff, got a blank card and searched an empty workspace before finding "New block" — 45 s lost.
- **Framework tags:** A6, A10, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel shows only "Nothing here yet."; no button or hint to create a note.
  - Novice searched "meeting" at 01:20 before trying the nav; reached "New block" at 01:40.
  - Contrasts with the arrival promise "never start from zero".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:1`
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a new workspace.
  2. Land on the dashboard.
  3. Observe "Nothing here yet." with no call to action.
- **Fix:** Put a "Write your first note" button inside the empty "Your cards" panel.

### 7e112a5c789f — One object carries three names: "Cards", "New block" and "notes"
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, adding hesitation to her first action.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** /app/dashboard.html#nav
- **Personas hit:** novice
- **Observed:**
  - Top nav reads "Cards", "New block"; dashboard search placeholder reads "Search your notes"; list heading "Your cards".
  - Novice paused on the nav at 01:40 and asked whether they were the same.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` (t 01:40)
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Open the dashboard.
  2. Read the nav ("Cards", "New block") and the search placeholder ("Search your notes").
- **Fix:** Pick one noun ("note") and use it in the nav, the create button, the list heading and the search placeholder.

### 162aa26454ac — Settings toggles are unexplained jargon and do not reflect the signup choice
- **Severity:** P2
- **So what:** Neither persona could tell what the toggles do or whether they relate to the irreversible signup choice.
- **Framework tags:** A2, A4, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Toggles "Enable webhook sync", "Federated graph replication" (checked), "Vault attestation"; no descriptions.
  - "Federated graph replication" is checked in both captures, though the novice chose "Hybrid mesh" and the power-user "Federated graph".
  - Both found "Export — Markdown, all cards" clear.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-power-user/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-power-user/session.log:13` · `persona-novice/findings-raw.json` (t 05:20) · `persona-power-user/findings-raw.json` (t 02:00)
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link." — power-user
  > "Webhook sync, graph replication, vault attestation — no idea. Export is clear." — novice
- **Repro:**
  1. Create a workspace choosing "Hybrid mesh".
  2. Open Settings.
  3. Observe "Federated graph replication" checked with no explanation.
- **Fix:** Add a one-line description under each toggle and show the chosen workspace type explicitly at the top of Settings.

### 7b3a05d59906 — No keyboard shortcuts for new note or search
- **Severity:** P2
- **So what:** The power user evaluating for his team expected keyboard-driven capture and found none.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - Tried Ctrl+K, Ctrl+N and "/" at 01:30; nothing happened.
  - Pre-session expectation was "fast capture, good search, keyboard-driven".
- **Evidence:** `persona-power-user/session.log:12` · `persona-power-user/session.log:3` · `persona-power-user/screenshots/02-dashboard.png`
  > "No keyboard shortcuts at all."
- **Repro:**
  1. Open the dashboard.
  2. Press Ctrl+K, Ctrl+N or "/".
  3. Observe no response.
- **Fix:** Bind "/" or Ctrl+K to focus search and Ctrl+N to open "New block"; list them in a "?" overlay.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Toast visibility/duration of "Saved ✓" — `04-note-saved-toast.png` shows the blank form, no toast captured.
- Live preview behaviour while typing — screenshot `03-new-note.png` shows "0 words" and an empty preview; only session.log:16 describes it (positive, not a finding).
- Whether Export actually produces Markdown — neither persona clicked it.

## For other lenses
- `POST /api/notes → 500` twice and `renderGraphOverlay is not defined` on dashboard — bugs.
- "Federated graph", "Sovereign vault", "Vault attestation" jargon density — content.
- Workspace-type step before any value; empty first-run — onboarding.
- Accessibility (radio buttons visually detached from their labels) — no lens covers it.

## Coverage gaps
- Export never clicked by either persona.
- Note edit, delete and the "Cards" nav item never opened.
- Mobile not tested; desktop 1440×900 only.
- Power-user captured no screenshot of the Memories page or the save toast.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice 00, 00-wall-cleared, 01–07 · power-user 00, 02, 03, 07
