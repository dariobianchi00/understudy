# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Nielsen A2 / A4 / A9 plus promise-vs-delivery (first-value Q4)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | Empty "Nothing here yet.", notes lost after "Saved ✓", Memories of facts that are not hers | Fail | Gave up at 06:30; would pay nothing |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Note lost after "Saved ✓", search finds nothing, Memories "Not me" | Fail | Gave up at 03:00; would pay nothing |

- Persona Q4 agrees with this reading for both: novice "No — it started completely empty, it lost what I gave it"; power-user "It remembers nothing I gave it and claims things I didn't."
- Root cause: the one word the pitch sells — "remembers" — is contradicted on three surfaces: empty start, lost saves, invented memories.

---

## Findings

### 62b222e9a047 — "Saved ✓" confirms a note that never appears in "Your cards" or search
- **Severity:** P0
- **So what:** The confirmation copy asserts something false, so both personas stopped believing anything the product says and quit.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - "Saved ✓" shown, then dashboard still reads "Nothing here yet." — twice for novice, once for power-user
  - Search for the saved title returns "No results for 'Dentist'." / no results for "Roadmap" — no explanation, no next step
  - Both personas gave up on the objective (`timeline.json` objectives `gave_up: true`)
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  > "Save doesn't save and search doesn't search."
- **Repro:**
  1. Open "New block", enter a title and body, click Save.
  2. Note the "Saved ✓" message; return to the dashboard.
  3. "Your cards" reads "Nothing here yet."; search the title — "No results for '<title>'".
- **Fix:** Show "Saved ✓" only after the note is persisted and listed in "Your cards"; on failure, show an error saying the note was not saved and how to retry.

### 8721043f4cef — Memories page states three false facts about a novice who wrote one note
- **Severity:** P0
- **So what:** Confident claims about her own life that are false made her doubt every other message, including "Saved".
- **Framework tags:** A2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** Memories page
- **Personas hit:** novice
- **Observed:**
  - Heading "What Nimbus remembers about you" over "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer "Memories are built from your notes and connected accounts." — she had no saved notes and connected no accounts
  - She stopped two minutes later: "I'd stop here."
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a fresh workspace; connect nothing.
  2. Click "Memories" in the top nav.
  3. Read three specific claims about the user with no source.
- **Fix:** Show only memories derived from this user's notes, each linked to its source note; when there are none, show an empty state saying so.

### f357201a86b8 — Memories page asserts facts a power user dismisses as a demo and will not trust
- **Severity:** P1
- **So what:** The feature that embodies the "remembers everything" pitch is written off on sight by the evaluator choosing for a team.
- **Framework tags:** A2, B-G11
- **Flow:** shape_2b
- **Locator:** Memories page
- **Personas hit:** power-user
- **Observed:**
  - Same three claims: "Tuesday meetings, Jira, Q4 launch"
  - Persona classed it as placeholder content and stated distrust
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md`
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a fresh workspace.
  2. Click "Memories".
- **Fix:** Label any sample memories as examples, or remove them; show real memories with a link to the note each came from.

### 09d9d2ece5c2 — Empty first screen contradicts the "never start from zero" promise for the novice
- **Severity:** P1
- **So what:** The first screen after signup is literally zero, the opposite of the pitch that brought her, and she named it in Q4.
- **Framework tags:** A2, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Pre-session expectation: "a notes app that fills itself in from things I already have"
  - Dashboard: "Your cards" — "Nothing here yet."; no import or connect option on screen
  - Q4 answer "No — it started completely empty"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:3` · `persona-novice/session.log:12` · `persona-novice/persona-debrief.md`
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Arrive from the marketing line "remembers everything so you never start from zero".
  2. Complete workspace signup.
  3. Land on an empty dashboard with no way to bring existing material in.
- **Fix:** Either change the marketing line to match an empty start, or make the first dashboard offer to import or connect existing notes.

### 414be1083fd9 — Irreversible workspace choice is offered only in unexplained jargon
- **Severity:** P2
- **So what:** A non-technical user makes a permanent decision by guessing, before seeing the product.
- **Framework tags:** A2, A5
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh" — no descriptions
  - "This cannot be changed later."
  - Novice picked "Hybrid mesh" "because it sounds like it includes the other two"
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it."
- **Repro:**
  1. Clear the login wall as a new user.
  2. Read the workspace-type screen.
- **Fix:** Add a plain-language line under each workspace option saying what it means for the user, and a default recommendation.

### 603b974be43f — Empty state "Nothing here yet." gives no next step
- **Severity:** P2
- **So what:** The activation moment says nothing about how to create a first note; the novice spent 45s hunting.
- **Framework tags:** A9, A10, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Empty state is three words, no action or link
  - Novice tried search first, then guessed "New block" at 01:40
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14`
  > "Nothing tells me what to do."
- **Repro:**
  1. Create a new workspace.
  2. Read the "Your cards" panel.
- **Fix:** Make the "Your cards" empty state say how to create the first note and link straight to the editor.

### 9a7502fa26aa — One object is called "cards", "block" and "notes" across four surfaces
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing before creating anything.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** top nav
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards", "New block"; dashboard heading "Your cards"; search placeholder "Search your notes"
  - Editor heading "New block"; export label "Markdown, all cards"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Cards and blocks — same thing?"
- **Repro:**
  1. Open the dashboard; compare nav labels, heading and search placeholder.
  2. Click "New block"; open Settings and read the export label.
- **Fix:** Pick one noun for a note and use it in the nav, editor heading, dashboard heading, search placeholder and export label.

### 7f24430d6a4b — Settings toggles use engineering jargon with no description
- **Severity:** P2
- **So what:** A non-technical user cannot tell what any setting does, so she cannot safely change one.
- **Framework tags:** A2
- **Flow:** shape_2b
- **Locator:** Settings page
- **Personas hit:** novice
- **Observed:**
  - Toggles "Enable webhook sync", "Federated graph replication", "Vault attestation" — no helper text
  - "Federated graph replication" pre-checked
  - Only "Export" / "Markdown, all cards" understood
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24`
  > "No idea. There's an Export button — "Markdown, all cards". At least that's clear."
- **Repro:**
  1. Click "Settings" in the top nav.
- **Fix:** Add one plain-language sentence under each Settings toggle saying what it changes for the user.

### 8168d2bf6b68 — "Federated graph replication" setting is not linked to the signup choice of the same name
- **Severity:** P3
- **So what:** The power user could not tell whether Settings reflects or overrides his permanent signup choice.
- **Framework tags:** A4
- **Flow:** shape_2b
- **Locator:** Settings page
- **Personas hit:** power-user
- **Observed:**
  - Signup option "Federated graph"; Settings toggle "Federated graph replication", checked
  - No copy relates the two
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:13`
  > "I picked that at signup — is this the same thing?"
- **Repro:**
  1. Pick "Federated graph" at signup.
  2. Open Settings.
- **Fix:** State on the Settings page which workspace type was chosen and whether this toggle is related to it.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Exact wording and placement of the "Saved ✓" toast — `persona-novice/screenshots/04-note-saved-toast.png` shows the blank "New block" form, no toast
- Exact "No results for '…'" copy layout — no screenshot shows it; only `session.log` lines
- Marketing-site copy beyond the one promise line — never captured

## For other lenses
- Notes not persisted after Save; search returns nothing — bugs
- Settings shows "Federated graph replication" checked although novice picked "Hybrid mesh" — bugs
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux
- Irreversible choice before first value — onboarding

## Coverage gaps
- Marketing site and pricing copy never opened
- Error copy for a failed save never surfaced, so not assessable
- Only desktop 1440x900 tested

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice 00–07; power-user 00, 02, 03, 07
