# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Nielsen A1/A2/A4/A9 + HAX B-G2/B-G11 (Memories is an inference surface) + Layer C; promise-vs-delivery first
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: ⚠ generic — INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope exclusion applied: "The login wall at /app/login.html — infrastructure, not a defect."

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | "Nothing here yet."; two notes "Saved ✓" then gone; Memories lists three false facts about her | Fail | Gave up at 06:30; "Nothing, until saving works" |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Save says "Saved ✓" but stores nothing; search returns "No results"; Memories "Not me" | Fail | Stopped at 03:00; "No. Nothing." |

- Both personas' own Q4 answers agree: "No". No disagreement with my reading.
- Root cause: the pitch is "remembers everything". The product's words claim remembering ("Saved ✓", "What Nimbus remembers about you") that the product does not deliver.
- Findings 1–4 below are symptoms of that one gap. Fix the claims and the delivery together, not screen by screen.

---

## Findings

### 242825d26356 — "Saved ✓" confirms a save that failed, and no error copy is ever shown
- **Severity:** P0
- **So what:** Both personas lost every note they wrote and were told it was safe; the novice concluded "It is lying to me."
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows green "Saved ✓"; every `POST /api/notes` returned 500 (novice 03:05, 03:50; power-user 01:00)
  - No error message, retry prompt or warning on any screen; "Your cards" stays "Nothing here yet."
  - Screenshot `04-note-saved-toast.png` does not show the toast — the toast copy is evidenced by the session log only
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-novice/network-full.txt` (`[POST] /api/notes → 500`, 2×) · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-power-user/network-full.txt` · `persona-power-user/screenshots/03-search-empty.png`
  > "Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me." (novice)
  > "Save doesn't save and search doesn't search." (power-user)
- **Repro:**
  1. Open New block, enter a title and body
  2. Click Save while `/api/notes` returns 500
  3. "Saved ✓" appears; the dashboard shows "Nothing here yet."
- **Fix:** Show "Saved ✓" only after the server confirms the save; on failure, show an error on the New block screen saying the note was not saved and offering a retry.

### 68cd0ff5f459 — Memories presents three invented facts as "What Nimbus remembers about you" (novice)
- **Severity:** P0
- **So what:** The false claims broke her trust in everything else the product says, including "Saved".
- **Framework tags:** A2, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Heading "What Nimbus remembers about you" over "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footnote "Memories are built from your notes and connected accounts." — she had zero saved notes and connected no accounts
  - She stopped 100 seconds later
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a new workspace, connect nothing
  2. Open Memories
  3. Three specific personal claims are shown as fact
- **Fix:** Never show sample memories as the user's own; until real memories exist, replace the list with an empty state that says how memories get created.

### 6766abbf734b — Memories presents three invented facts as "What Nimbus remembers about you" (power-user)
- **Severity:** P1
- **So what:** He wrote the feature off as a fake demo, so the product's headline promise lost its only visible proof.
- **Framework tags:** A2, B-G2, B-G11
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three statements, same footnote "Memories are built from your notes and connected accounts."
  - Read it as "a demo panel" and explicitly declined to trust it
  - The rubric's P0 example ("confident nonsense about the persona's own data") was considered; his trust in the rest of the product did not collapse, so P1
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` (t 02:30) · `persona-power-user/persona-debrief.md` (Q4)
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
  > ""Remembers everything." No. It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Create a new workspace, connect nothing
  2. Open Memories
- **Fix:** Same as the novice variant: remove sample memories and label any example content plainly as an example.

### b0eff85ad56f — "Never start from zero" pitch meets a blank "Nothing here yet." dashboard (novice)
- **Severity:** P1
- **So what:** She came for a notes app that "fills itself in", met an empty one, and named this mismatch in her Q4 "No".
- **Framework tags:** A2, B-G1, C-SOWHAT
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Pre-session expectation: "a notes app that fills itself in from things I already have"
  - First screen after signup: "Your cards" — "Nothing here yet." No import, no connect step, no explanation of how it gets filled
  - Power-user expected an empty start ("Expected, nothing's in it yet") — severity flip, no finding for him
- **Evidence:** `persona-novice/session.log:2` · `persona-novice/session.log:3` · `persona-novice/session.log:12` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/persona-debrief.md` (Q4)
  > "I thought it would have my stuff."
  > "No — it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine."
- **Repro:**
  1. Arrive from the marketing site ("remembers everything so you never start from zero")
  2. Complete signup
  3. The dashboard reads "Nothing here yet."
- **Fix:** Either bring the marketing promise in line with a blank start, or make the first dashboard explain how Nimbus fills itself and offer that step there.

### 7fac048a14e4 — Irreversible signup choice uses unexplained jargon: "Federated graph", "Sovereign vault", "Hybrid mesh" (novice)
- **Severity:** P2
- **So what:** She made a permanent choice by guessing from the sound of the words, before seeing the product.
- **Framework tags:** A2, A5
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Heading "Before we begin, choose your workspace type"; three options with no descriptions
  - Warning "This cannot be changed later." directly above "Create workspace"
  - Took 43 s (00:05–00:48); picked "Hybrid mesh" "because it sounds like it includes the other two"
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall; land on /app/signup.html
  2. Read the three options
- **Fix:** Give each workspace type a plain-language one-line description of what it changes for the user, or default the choice and move it out of signup.

### f1889bbd6786 — Irreversible signup choice uses unexplained jargon: "Federated graph", "Sovereign vault", "Hybrid mesh" (power-user)
- **Severity:** P3
- **So what:** He shrugged it off; it did not change his behaviour, but it reads as an unfinished product.
- **Framework tags:** A2
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Same screen, same "This cannot be changed later."
  - Chose "Federated graph" without hesitating
- **Evidence:** `persona-power-user/session.log:8`
  > "Fine — I've seen worse. Picked Federated graph."
- **Repro:**
  1. Land on /app/signup.html
- **Fix:** Same as the novice variant: add a plain one-line description under each option.

### fd490e4e5a4b — Settings labels are infrastructure jargon: "Enable webhook sync", "Federated graph replication", "Vault attestation"
- **Severity:** P2
- **So what:** A non-technical user cannot tell what any toggle does, so cannot tell if her data is safe.
- **Framework tags:** A2, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice
- **Observed:**
  - Three toggles, labels only, no help text; "Federated graph replication" is on by default
  - The only label she understood: Export — "Markdown, all cards"
  - 3 of 4 controls need product-internal or infra knowledge to parse
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24`
  > ""Enable webhook sync", "Federated graph replication", "Vault attestation". No idea. There's an Export button — "Markdown, all cards". At least that's clear."
- **Repro:**
  1. Open Settings
- **Fix:** Add a one-line plain-language description under each Settings toggle saying what it does for the user's notes.

### 8c83dc277f62 — The same item is called "cards", "block" and "notes" across nav, editor and search
- **Severity:** P2
- **So what:** She couldn't tell whether "New block" made the thing listed under "Your cards", which added to her confusion when it never appeared.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** /app/dashboard.html nav
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards", "New block"; dashboard heading "Your cards"; search placeholder "Search your notes"
  - Editor heading "New block"; Export label "Markdown, all cards"
  - Product name is "Nimbus Notes"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Open the dashboard and read the nav, heading and search placeholder
  2. Click "New block"
- **Fix:** Pick one noun for a user's note and use it in the nav, editor heading, list heading, search placeholder and export label.

### abe002d1e5f9 — Settings "Federated graph replication" reuses the signup term "Federated graph" with no stated link
- **Severity:** P2
- **So what:** He could not tell if his permanent signup choice was in fact a toggle, which undermines the "cannot be changed" warning.
- **Framework tags:** A4, A2
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - Signup option "Federated graph" with "This cannot be changed later."
  - Settings toggle "Federated graph replication", checked by default, no description
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:13` · `persona-novice/screenshots/01-signup-workspace-type.png`
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Pick "Federated graph" at signup
  2. Open Settings
- **Fix:** Rename the Settings toggle so it doesn't reuse the signup term, or state under it how it relates to the chosen workspace type.

### 5f9be60ab6aa — Dashboard empty state "Nothing here yet." gives no way to fill it
- **Severity:** P2
- **So what:** Her first screen gave no next step, so she searched an empty list before finding "New block" at 01:40.
- **Framework tags:** A2, A6, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" → "Nothing here yet." — no button, link or instruction in the card
  - She typed "meeting" into search first: "No results for 'meeting'."
  - 45 s from dashboard (00:55) to clicking "New block" (01:40)
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14`
  > "'Nothing here yet.' Nothing tells me what to do."
- **Repro:**
  1. Complete signup
  2. Read the "Your cards" card
- **Fix:** Put a create-your-first-note action and one line on what goes here inside the empty "Your cards" card.

---

## What works
- Export copy "Markdown, all cards" was the one label both personas understood (`persona-novice/session.log:23`, `persona-power-user/session.log:13`)
- Editor live counter "0 words" / "Preview below" gave the novice her only moment of value at 02:41 (`persona-novice/session.log:16`)

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Toast wording "Saved ✓" is not visible in `04-note-saved-toast.png` (it shows the empty editor) — the wording rests on session.log only; kept in the finding with the screenshot caveat
- Search no-results copy ("No results for 'Dentist'.") offers no next step — only seen after failed saves, so the content effect can't be separated from the save failure

## For other lenses
- `POST /api/notes` → 500 on every save; `Uncaught ReferenceError: renderGraphOverlay is not defined` on dashboard — bugs
- No keyboard shortcuts (Ctrl+K, Ctrl+N, / do nothing), `persona-power-user/session.log:12` — ux
- Irreversible decision before first value at signup — onboarding
- Radio buttons and checkboxes sit centred, detached from their labels (`01-signup-workspace-type.png`, `07-settings.png`) — ux

## Coverage gaps
- Marketing site copy never captured — the promise is known only from the persona pre-session line
- No error copy observed anywhere: either none exists or capture never triggered it
- Mobile not tested; both personas on desktop-1440x900
- Power-user screenshots exist only for start, dashboard, search, settings — Memories and signup content for him cite session.log

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast, 05-notes-list-missing, 06-memories, 07-settings · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
