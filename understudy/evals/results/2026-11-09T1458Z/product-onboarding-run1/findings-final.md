# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C activation (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT) with A/B tags where they apply
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on invented personas
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Auth wall at /app/login.html excluded (scope exclusion); clock starts after it

---

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached signup (after wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen (irreversible) | ✓ 00:48 — guessed "Hybrid mesh" | ✓ <00:30 — "Federated graph" |
| Dashboard reached | ✓ 00:55 — "Nothing here yet." | ✓ 00:30 — empty |
| Note written in "New block" | ✓ 01:55–02:41 | ✓ 01:00 |
| Note saved and listed | ✗ 03:05 / 03:50 — "Saved ✓" twice, list empty | ✗ 01:00 — "Saved ✓", list empty |
| **First value: note found again** | ✗ 03:30 search "Dentist" → no results | ✗ 01:00 search "Roadmap" → no results |
| Session end | ✗ abandoned 06:30 ("I'd stop here") | ✗ abandoned 03:00 ("Enough.") |

**Steps to value (required path):** 5 — choose workspace type · Create workspace · New block · write · Save · **Time to value:** not reached (see note) · **Drop-off:** Save → empty list, both personas

- Capture recorded novice `seconds_to_first_value: 161` (02:41, live word-count/preview); persona rejected it in debrief Q1: "right now: nothing"
- Power-user `first_value_reached: false` (`timeline.json`)
- Both are **abandonments**, not time-outs: 06:30 and 03:00 of a 90-minute cap
- Novice wandered: searched an empty workspace for "meeting" at 01:20 (`times_had_to_hunt: 2`); power-user searched "test" at 00:45 (`times_had_to_hunt: 1`)

---

## Findings

### 193f7ecc7a87 — Save shows "Saved ✓" but the note is never stored, so no persona reaches first value
- **Severity:** P0
- **So what:** Both personas wrote a note, were told it saved, saw it vanish, and quit — activation is 0 of 2.
- **Framework tags:** A1, C-TTFV, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows green "Saved ✓"; network shows `POST /api/notes → 500` every time (03:05, 03:50 novice; 01:00 power-user)
  - Dashboard returns to "Nothing here yet."; search for the note title returns no results
  - Novice abandoned at 06:30, power-user at 03:00 — both well inside the 90-min cap
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-power-user/network-full.txt:3` · `persona-novice/timeline.json` objectives[0].gave_up = true
  > "Saved twice, empty twice. It is lying to me."
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work."
- **Repro:**
  1. Sign up, choose any workspace type, Create workspace
  2. Click "New block", enter a title and body, click Save
  3. Observe "Saved ✓", then the dashboard still reads "Nothing here yet."; search the title → no results
- **Fix:** Show "Saved ✓" only after `POST /api/notes` returns 2xx; on failure show an error and keep the draft in the form.

### fa590f624397 — Memories invents facts about a brand-new user, and the novice stops trusting "Saved" too
- **Severity:** P0
- **So what:** Fabricated "memories" convinced the novice the product makes things up, so she stopped believing its confirmations at all.
- **Framework tags:** A1, B-G11, C-ABANDON, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** nav: Memories
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — she had zero saved notes and no connected accounts
  - Debrief Q4: Fail — "the 'memories' it does have aren't mine"
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a new workspace; do not save any notes
  2. Click "Memories" in the top nav
  3. Observe three specific claims about the user
- **Fix:** On a new workspace, replace the seeded memories with an empty state: "Nimbus will remember things here once you've saved a few notes."
- P0 not P1 because the rubric's "confident nonsense about the persona's own data" applies; it did not by itself cause abandonment — Save did.

### cb7512d916b0 — Memories invents facts the power user rejects as a demo panel he will not trust
- **Severity:** P1
- **So what:** The headline "remembers everything" feature is written off on first sight by the team evaluator.
- **Framework tags:** B-G11, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** nav: Memories
- **Personas hit:** power-user
- **Observed:**
  - Same three seeded memories (Tuesday meetings, Jira, Q4 launch)
  - Dismissed as a demo panel rather than alarming — severity flip vs novice (P0)
  - Debrief Q4: "It remembers nothing I gave it and claims things I didn't."
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` Q4
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a new workspace
  2. Click "Memories"
- **Fix:** Label any sample memories "Example" or remove them until the user's own notes produce real ones.
- Screenshot is the novice's capture of the same page; power-user did not screenshot Memories.

### d5ed336e6413 — Signup forces an irreversible, unexplained workspace type before the novice has seen the product
- **Severity:** P2
- **So what:** A non-technical newcomer spends 43 s guessing at a permanent choice; a less patient one leaves before the product loads.
- **Framework tags:** A2, B-G11, C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh" — no descriptions
  - "This cannot be changed later." directly under the options
  - Novice hesitated 00:05 → 00:48 and picked by guess; pushed through, so P2 not P1
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the auth wall to /app/signup.html
  2. Read the three options and the "cannot be changed later" line
- **Fix:** Default the workspace type silently and move the choice to Settings, or add one plain-English line per option and make it changeable.
- Severity flip: power-user "Fine — I've seen worse." (`persona-power-user/session.log:8`) — non-issue at signup; his variant is below.

### 16821e1babda — Workspace type chosen at signup never reappears by name, so the power user cannot tell what it controls
- **Severity:** P3
- **So what:** The one irreversible onboarding decision has no visible effect, which undercuts why it was demanded.
- **Framework tags:** A4, B-G11
- **Flow:** shape_2b
- **Locator:** nav: Settings
- **Personas hit:** power-user
- **Observed:**
  - Settings shows "Federated graph replication" pre-ticked, alongside "Enable webhook sync" and "Vault attestation"
  - Nothing names the workspace type chosen at signup
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-power-user/session.log:13`
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Sign up choosing "Federated graph"
  2. Open Settings
- **Fix:** Show "Workspace type: Federated graph" at the top of Settings with one line on what it changes.
- Power-user's `07-settings.png` was listed but the novice's capture of the same page is cited, which I opened.

### ab57d762079a — First screen after signup says "Nothing here yet." and offers no next step
- **Severity:** P2
- **So what:** The novice's first action was searching an empty workspace; 45 s lost before finding "New block".
- **Framework tags:** A6, B-G1, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Dashboard: "Search your notes" box, "Your cards", "Nothing here yet." — no button or hint to create one
  - Novice searched "meeting" at 01:20, then reached "New block" at 01:40
  - `times_had_to_hunt: 2` in `timeline.json`
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13`
  > "'Nothing here yet.' Nothing tells me what to do."
- **Repro:**
  1. Create a workspace
  2. Land on the dashboard
- **Fix:** Replace "Nothing here yet." with a "Write your first note" button that opens New block.

### 0c75b4ee9b74 — Cards, blocks and notes name one thing three ways, stalling the novice at the menu
- **Severity:** P2
- **So what:** The novice could not tell whether "New block" makes the "cards" listed or the "notes" searched.
- **Framework tags:** A4, C-STEPS
- **Flow:** shape_1
- **Locator:** nav: Cards · New block
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards", "New block"; dashboard: "Search your notes", "Your cards"; Settings: "Markdown, all cards"
  - Novice paused at 01:40 before choosing "New block"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` t=01:40
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Land on the dashboard
  2. Compare nav labels with the search placeholder and list heading
- **Fix:** Use "note" everywhere: "Notes", "New note", "Search your notes", "Your notes".

### 826870926193 — Empty first workspace contradicts the "never start from zero" promise the novice arrived with
- **Severity:** P2
- **So what:** The pitch set an expectation of pre-filled content; an empty start reads as broken before any real failure.
- **Framework tags:** C-SOWHAT, B-G1
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Arrived expecting "a notes app that fills itself in from things I already have"
  - First screen: "Nothing here yet."; no import or connect option on the dashboard
  - Debrief Q4: Fail — "it started completely empty"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:3` · `persona-novice/session.log:12` · `persona-novice/persona-debrief.md` Q4
  > "I thought it would have my stuff."
- **Repro:**
  1. Arrive from the marketing line "remembers everything so you never start from zero"
  2. Create a workspace and land on the empty dashboard
- **Fix:** Offer an import step (paste, upload Markdown) on the empty dashboard, or soften the marketing line to match an empty start.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "Saved ✓" toast appearance — `persona-novice/screenshots/04-note-saved-toast.png` actually shows an empty New block form, no toast; toast rests on `session.log:17` only
- Search "No results for '…'" message — neither `05-notes-list-missing.png` nor `03-search-empty.png` shows a query or result text; rests on session logs only

## For other lenses
- `POST /api/notes → 500` and `Uncaught ReferenceError: renderGraphOverlay is not defined` on dashboard — bugs
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) for the keyboard-driven evaluator (`persona-power-user/session.log:12`) — ux
- Settings jargon: "Enable webhook sync", "Vault attestation" — content
- Radio buttons and checkboxes render centred, detached from their labels (`01-signup-workspace-type.png`, `07-settings.png`) — ux

## Coverage gaps
- No persona reached a second task or returned; retention stage unobservable
- Export ("Markdown, all cards") never clicked by either persona
- Power-user did not screenshot Memories or the New block form
- Desktop 1440×900 only; no mobile run

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice 00–07 (00-wall-cleared, 01 signup, 02 dashboard, 03 new note, 04 new-note form, 05 empty list, 06 memories, 07 settings) · power-user 00, 02, 03, 07
