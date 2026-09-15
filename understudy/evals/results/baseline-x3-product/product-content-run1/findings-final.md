# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: promise-vs-delivery (first-value Q4) + Nielsen A2/A4/A9 for copy, reading level, jargon density
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user; both desktop-1440x900)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Layer B (HAX) applied only to the Memories surface — the one place the product presents inferred output as its own

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | Empty dashboard "Nothing here yet."; two notes "Saved ✓" then gone; Memories about someone else | **Fail** | Gave up at 06:30 with zero notes; "I'd stop here" |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Empty dashboard; note lost after "Saved ✓"; search finds nothing; no shortcuts | **Fail** | Gave up at 03:00; "Nothing else matters until those work" |

- Persona Q4 answers: novice "No", power-user "No". Analyst reading agrees with both; no disagreement to note.
- Root cause chain: pitch says *remembers* → product loses the note (6eb032a62e2a) → then *remembers* things that are not theirs (b5fd33310c0b). Every other finding is downstream of that contradiction.

## Reading level and jargon

- Sentence-level reading level is low (≈ grade 5–6): short declaratives — "Nothing here yet.", "This cannot be changed later.", "Preview below".
- The difficulty is nouns, not syntax. 8 terms across 3 screens that a non-technical persona could not explain: "Federated graph", "Sovereign vault", "Hybrid mesh", "webhook sync", "Federated graph replication", "Vault attestation", "cards", "block".
- Novice's own count on Settings: "words I don't know, one button I do" (`persona-novice/session.log:24`).
- Error copy: none exists — the only failure state observed (`POST /api/notes → 500`) rendered as success copy.
- Empty-state copy: "Nothing here yet." and "No results for '…'." — both name the state, neither names a next step.

---

## Findings

### 6eb032a62e2a — "Saved ✓" confirms a save the server rejected, and no error copy exists
- **Severity:** P0
- **So what:** Both personas were told their note was kept when it was not; both called the product a liar and quit.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Green "Saved ✓" toast shown top right after Save; the request behind it returned `POST /api/notes → 500`.
  - No error message anywhere: dashboard still reads "Nothing here yet.", search returns "No results for 'Dentist'."
  - Novice repeated the save twice and got the same success copy both times.
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-power-user/network-full.txt:3` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/persona-debrief.md:4`
  > "Saved twice, empty twice. It is lying to me." — novice
  > "Nothing yet — it accepts a note and then loses it." — power-user
- **Repro:**
  1. Sign up, choose any workspace type, open "New block".
  2. Enter a title and body, click "Save".
  3. Observe "Saved ✓" toast while the network panel shows `POST /api/notes 500`; return to dashboard — list is empty.
- **Fix:** On the New block form, show "Saved ✓" only after a 2xx from `/api/notes`; on any error, replace it with a message that says the note was not saved and offers Retry.

### 2b34734eadd1 — Product contradicts its own pitch "remembers everything so you never start from zero"
- **Severity:** P1
- **So what:** Both personas arrived expecting to find something and found nothing — the first screen breaks the promise before the bug does.
- **Framework tags:** A2, C-SOWHAT, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - First screen after signup: "Your cards" — "Nothing here yet."; no copy explains how Nimbus will come to remember anything.
  - Novice expected "a notes app that fills itself in from things I already have"; no import, connect or "start from" path is offered.
  - Both personas answered Q4 "No"; power-user: "It remembers nothing I gave it and claims things I didn't."
- **Evidence:** `persona-novice/session.log:2` · `persona-novice/session.log:3` · `persona-novice/session.log:12` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-power-user/screenshots/02-dashboard.png` · `persona-novice/persona-debrief.md:13` · `persona-power-user/persona-debrief.md:13`
  > "No — it started completely empty, it lost what I gave it, and the 'memories' it does have aren't mine." — novice
- **Repro:**
  1. Read the marketing line "Nimbus remembers everything so you never start from zero".
  2. Sign up and land on `/app/dashboard.html`.
  3. Observe an empty list and no explanation of what Nimbus will remember or from where.
- **Fix:** Either make the dashboard's first state deliver on "never start from zero" (import/connect step with copy naming the source) or change the marketing line to describe what a new account actually contains.

### b5fd33310c0b-a — Memories page asserts facts about the user drawn from nothing they provided
- **Severity:** P0
- **So what:** Novice now doubts every other message the product shows — "is it making up the 'Saved' too?" — trust is gone for the session.
- **Framework tags:** A2, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Heading "What Nimbus remembers about you" with three claims: "You prefer to schedule meetings on Tuesday afternoons." "Your team uses Jira and Slack." "You are working on a product launch in Q4."
  - Footer copy "Memories are built from your notes and connected accounts." — no accounts were connected; the one note was about a dentist and was lost.
  - No label marks this as sample, demo or placeholder content.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:24`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?" — novice
- **Repro:**
  1. Sign up with a fresh account; connect nothing.
  2. Click "Memories" in the top nav.
  3. Observe three second-person claims about the user and a footer attributing them to "your notes and connected accounts".
- **Fix:** On `/app/memories.html`, show an empty state for accounts with no source data, and label any sample content as sample; delete the footer claim until it is true.

### b5fd33310c0b-b — Memories page asserts facts about the user drawn from nothing they provided
- **Severity:** P1
- **So what:** Power-user wrote the page off as "a demo panel" and stated they would not trust it — the headline feature is dismissed on first sight.
- **Framework tags:** A2, B-G2, B-G11
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three claims ("Tuesday meetings, Jira, Q4 launch") shown to a second fresh account with different notes.
  - Persona guessed the content was a demo; nothing on the page says so.
  - Debrief Q4: "It remembers nothing I gave it and claims things I didn't."
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json:24` · `persona-power-user/persona-debrief.md:13` · `persona-novice/screenshots/06-memories.png`
  > "Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it." — power-user
- **Repro:**
  1. Sign up with a second fresh account; write one note titled "Roadmap".
  2. Click "Memories".
  3. Observe the identical three claims shown to the first account.
- **Fix:** Same surface as b5fd33310c0b-a — if the content is illustrative, say "Example" on each card; otherwise show nothing until real memories exist.

### a0a9df6b0d8e-a — Irreversible workspace choice offered in three undefined terms
- **Severity:** P1
- **So what:** Novice guessed at a decision the copy says cannot be undone, 5 seconds into the product — a plausible walk-away point.
- **Framework tags:** A2, A5, A6, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Heading "Before we begin, choose your workspace type"; options "Federated graph", "Sovereign vault", "Hybrid mesh"; no description under any option.
  - Helper text "This cannot be changed later." is the only explanatory copy on the screen.
  - Novice spent 43 s deciding, then "Picked 'Hybrid mesh' because it sounds like it includes the other two."
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-novice/findings-raw.json:6`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo." — novice
- **Repro:**
  1. Clear the login wall; land on `/app/signup.html`.
  2. Read the three radio labels — no definitions, tooltips or "which should I pick" copy.
- **Fix:** Under each of the three options on the signup screen, add one plain-language line saying what it means for the user and who should pick it; mark one as recommended.

### a0a9df6b0d8e-b — Irreversible workspace choice offered in three undefined terms
- **Severity:** P3
- **So what:** Power-user shrugged and picked one in 30 s, but still chose an unchangeable setting with no stated consequence.
- **Framework tags:** A2, A5
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Same screen, same three undefined labels and "cannot be changed" helper text.
  - Persona: "Fine — I've seen worse. Picked Federated graph."
  - The choice resurfaced later as the unexplained "Federated graph replication" toggle (see 0146ffa0b162).
- **Evidence:** `persona-power-user/session.log:8` · `persona-novice/screenshots/01-signup-workspace-type.png`
  > "Workspace type: Federated graph / Sovereign vault / Hybrid mesh, cannot be changed. Fine — I've seen worse." — power-user
- **Repro:**
  1. Land on `/app/signup.html` after the wall.
  2. Observe three labels with no description and "This cannot be changed later."
- **Fix:** Same change as a0a9df6b0d8e-a — one descriptive line per option on the signup screen.

### ad8c348546db — One object is called "notes", "cards" and "block" across four surfaces
- **Severity:** P2
- **So what:** Novice could not tell whether "New block" would create the thing listed under "Your cards" — the core object has no stable name.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards" and "New block"; dashboard heading "Your cards"; search placeholder "Search your notes"; Settings export "Markdown, all cards".
  - Three words for the same object on one screen (`02-dashboard-empty.png`), a fourth form ("block") in the creation flow.
  - Power-user saw the same screens and did not remark on it.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json:48`
  > "Cards, blocks, notes — are these the same thing?" — novice
- **Repro:**
  1. Open `/app/dashboard.html`; read the nav, the search placeholder and the list heading.
  2. Click "New block"; read the form heading.
- **Fix:** Pick one noun for the object (the marketing name is "Notes") and use it in the nav item, the creation button, the list heading, the search placeholder and the export label.

### 3853568a9ff0 — Empty state "Nothing here yet." names no next step
- **Severity:** P2
- **So what:** Novice sat on the first screen for 45 s not knowing what to do; the activation moment passed without a prompt.
- **Framework tags:** A6, A10, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Dashboard list body reads only "Nothing here yet." — no link, button or sentence pointing at "New block".
  - Novice tried search first ("meeting" → "No results for 'meeting'."), then hunted the nav.
  - Power-user was not affected: "Dashboard, empty. … Expected, nothing's in it yet."
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/findings-raw.json:12` · `persona-power-user/session.log:9`
  > "'Nothing here yet.' Nothing tells me what to do." — novice
- **Repro:**
  1. Sign up and land on `/app/dashboard.html` with no notes.
  2. Read the "Your cards" panel.
- **Fix:** Replace "Nothing here yet." with a line that says what goes here and a button that opens the create form.

### 80176917dc14 — Settings toggles use three undefined technical terms
- **Severity:** P2
- **So what:** Novice could act on one of four controls on the page; the other three are unreadable to them and one is on by default.
- **Framework tags:** A2, A6
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice
- **Observed:**
  - Toggle labels: "Enable webhook sync", "Federated graph replication" (checked by default), "Vault attestation"; no helper text on any.
  - Only "Export — Markdown, all cards" was understood.
  - Persona's own tally: "words I don't know, one button I do."
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24` · `persona-novice/findings-raw.json:42`
  > "'Enable webhook sync', 'Federated graph replication', 'Vault attestation'. No idea. There's an Export button — 'Markdown, all cards'. At least that's clear." — novice
- **Repro:**
  1. Open `/app/settings.html` as a non-technical user.
  2. Read the three checkbox labels.
- **Fix:** Add a one-line plain-language description under each of the three toggles saying what changes when it is on, or move them behind an "Advanced" section.

### 0146ffa0b162 — "Federated graph replication" toggle not tied on-screen to the signup "Federated graph" choice
- **Severity:** P2
- **So what:** Power-user could not tell whether unticking this box undoes the choice the product said "cannot be changed later".
- **Framework tags:** A4, A2
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - Signup: "Federated graph" chosen, "This cannot be changed later."
  - Settings: "Federated graph replication" checkbox, on by default, unchecked-able; no copy links it to the signup choice.
  - Same two words, two screens, no stated relationship.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:8` · `persona-power-user/session.log:13` · `persona-power-user/findings-raw.json:18`
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link." — power-user
- **Repro:**
  1. Sign up choosing "Federated graph".
  2. Open `/app/settings.html`; find the checked "Federated graph replication" box.
- **Fix:** On the Settings toggle, state in one line whether it is the workspace type from signup and what unticking it does; if it is the same thing, remove "cannot be changed later" from signup.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast copy itself — `04-note-saved-toast.png` shows the empty form, not the toast; the wording rests on `session.log:17` only. Kept in 6eb032a62e2a on the log line; a screenshot of the toast would strengthen it.
- Search empty state "No results for '…'." may need a "create it" link — only observed while the save bug masked whether search works at all.

## For other lenses
- `POST /api/notes → 500` on every save, both personas — **bugs**.
- `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load — **bugs**.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, / all inert) — **ux**.
- Novice TTFV 2:41 on the live preview, then value lost; power-user first value never reached — **onboarding**.
- Irreversible decision before any value shown (signup gate) — **ux**, **onboarding**.

## Coverage gaps
- No marketing page captured; the promise is known only from the pre-session line, not from on-page copy.
- Export flow never executed — "Markdown, all cards" copy seen, result not seen.
- Mobile not tested; both personas desktop 1440×900.
- `persona-novice/screenshots/04-note-saved-toast.png` is a duplicate of `03-new-note.png`; the toast was not captured.
- Power-user has no signup or Memories screenshot; those surfaces are cited from the novice capture and the power-user log.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index
  - `persona-novice/screenshots/00-start.png` — login wall (excluded)
  - `persona-novice/screenshots/00-wall-cleared.png` — workspace type screen
  - `persona-novice/screenshots/01-signup-workspace-type.png` — workspace type screen
  - `persona-novice/screenshots/02-dashboard-empty.png` — empty dashboard
  - `persona-novice/screenshots/03-new-note.png` — New block form, empty
  - `persona-novice/screenshots/04-note-saved-toast.png` — New block form, empty (toast not captured)
  - `persona-novice/screenshots/05-notes-list-missing.png` — empty dashboard after save
  - `persona-novice/screenshots/06-memories.png` — Memories page, three claims
  - `persona-novice/screenshots/07-settings.png` — Settings, three toggles + Export
  - `persona-power-user/screenshots/00-start.png` — login wall (excluded)
  - `persona-power-user/screenshots/02-dashboard.png` — empty dashboard
  - `persona-power-user/screenshots/03-search-empty.png` — empty dashboard after search
  - `persona-power-user/screenshots/07-settings.png` — Settings
