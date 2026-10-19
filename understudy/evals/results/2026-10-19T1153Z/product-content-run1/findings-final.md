# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: promise-vs-delivery (first-value Q4) · Nielsen A2/A4/A9 · reading level, jargon density, naming consistency
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | "Nothing here yet."; a note confirmed "Saved ✓" twice and never shown; Memories full of facts that are not hers | Fail | Gave up at 06:30: "I'd stop here"; would pay "Nothing, until saving works" |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Save confirmed but nothing kept; search finds nothing; Memories "Not me" | Fail | Stopped at 03:00: "Save doesn't save and search doesn't search"; would pay "Nothing" |

- Both personas' own Q4 answers say "No" — my reading agrees; no disagreement to reconcile.
- The mismatch is the root cause of F2–F4 and F9: the copy keeps asserting memory the product does not deliver.

## Reading level and jargon

- Nav, editor, Export copy: plain, ~grade 5. Both personas understood "Export · Markdown, all cards".
- Signup and Settings: specialist infrastructure vocabulary, unreadable for the novice persona.
- 8 jargon or internal terms on 4 screens: "Federated graph", "Sovereign vault", "Hybrid mesh", "Enable webhook sync", "Federated graph replication", "Vault attestation", "block", "cards".
- Novice could explain none of the first six: "I don't know what any of these are" · "No idea".

---

## Findings

### 730e6b7756d0 — Product contradicts its remembers-everything pitch: it starts empty and keeps nothing the persona writes
- **Severity:** P0
- **So what:** Both personas arrived for memory and left saying the product remembers nothing of theirs; neither would pay or return.
- **Framework tags:** A2, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Pitch both personas arrived with: "remembers everything so you never start from zero".
  - First screen after signup: "Your cards" · "Nothing here yet." — the product starts from zero.
  - Notes written and confirmed "Saved ✓" never reappear; both personas gave up on the objective.
- **Evidence:** `persona-novice/session.log:2` · `persona-novice/session.log:12` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md` · `persona-power-user/session.log:15` · `persona-power-user/persona-debrief.md`
  > "No — it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine." (novice, Q4)
  > ""Remembers everything." No. It remembers nothing I gave it and claims things I didn't." (power-user, Q4)
- **Repro:**
  1. Arrive from the marketing site promising "remembers everything so you never start from zero".
  2. Create a workspace; land on the dashboard.
  3. Write and save a note via "New block"; return to the dashboard.
- **Fix:** Until saving and import work, remove "remembers everything so you never start from zero" from the marketing site and onboarding.

### 29944f393d00 — Saved confirmation reports success for notes that never appear in the list or in search
- **Severity:** P0
- **So what:** The only feedback copy on save is a false success message, so the persona concludes the product is lying.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Clicking Save shows green "Saved ✓"; the dashboard then still reads "Nothing here yet."
  - Search for the saved title returns "No results for 'Dentist'." and finds nothing for "Roadmap".
  - No error, warning or next step appears anywhere; novice repeated the save and got "Saved ✓" again.
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
- **Repro:**
  1. Open "New block"; enter Title "Dentist" and a body.
  2. Click Save; note the "Saved ✓" toast.
  3. On the dashboard, observe "Nothing here yet."; search "Dentist" → "No results for 'Dentist'."
- **Fix:** Show "Saved ✓" only after the note is confirmed stored and visible; on failure show a plain error saying the note was not kept and how to retry.

### 5933a00d0b86 — Memories page states invented facts about the novice, so she stops trusting every other message
- **Severity:** P0
- **So what:** Confident claims about her that are false made her doubt the "Saved" message too — trust broke across the product.
- **Framework tags:** A2, B-G2, C-ABANDON
- **Flow:** shape_2b
- **Locator:** nav: Memories
- **Personas hit:** novice
- **Observed:**
  - Heading "What Nimbus remembers about you" over "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer "Memories are built from your notes and connected accounts." — she had connected no accounts and saved no note.
  - She extended the distrust to the save confirmation, then stopped two minutes later.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Sign up as a new user; connect nothing.
  2. Click "Memories" in the nav.
  3. Read the three statements and the footer.
- **Fix:** Never show sample statements as "What Nimbus remembers about you"; for a new account, show an empty state saying nothing is remembered yet and what will populate it.

### a1dbdf1010bf — Memories page states invented facts about the power user, who writes it off as an untrusted demo panel
- **Severity:** P1
- **So what:** The evaluator dismissed the product's headline feature as fake, removing the one reason to switch the team.
- **Framework tags:** A2, B-G2
- **Flow:** shape_2b
- **Locator:** nav: Memories
- **Personas hit:** power-user
- **Observed:**
  - Same three statements under "What Nimbus remembers about you".
  - He read them as a demo, not as his data, and said he would not trust the panel.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` · `persona-novice/screenshots/06-memories.png`
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Sign up as a new user; connect nothing.
  2. Click "Memories".
- **Fix:** Replace the placeholder memories with an honest empty state; label any sample content as an example, never as "about you".

### 9c0fa352bca8 — Signup forces an irreversible choice between three undefined jargon terms before the product is shown
- **Severity:** P2
- **So what:** The novice guessed a permanent setting from the sound of the words; a less patient user stops at step one.
- **Framework tags:** A2, A3, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh" — no descriptions.
  - Warning under the options: "This cannot be changed later."
  - Novice spent 43 s, then picked "Hybrid mesh" "because it sounds like it includes the other two".
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall; land on /app/signup.html.
  2. Read the three options and the warning.
- **Fix:** Give each workspace type a one-line plain-language description of what it means for the user, or default it and move the choice out of signup.

### 5700fe15f01d — Settings shows Federated graph replication ticked regardless of the workspace type chosen at signup, with no link between them
- **Severity:** P2
- **So what:** The signup term reappears with a different meaning and no explanation, so even the expert could not tell what he had chosen.
- **Framework tags:** A4, A2
- **Flow:** shape_2b
- **Locator:** nav: Settings
- **Personas hit:** power-user, novice
- **Observed:**
  - Settings checkbox "Federated graph replication" is ticked by default.
  - Power user chose "Federated graph" and asked whether it was the same thing; novice chose "Hybrid mesh" and sees it ticked too.
  - No copy on either screen connects the two terms.
- **Evidence:** `persona-power-user/session.log:13` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:11`
  > ""Federated graph replication" is on by default. I picked that at signup — is this the same thing?"
- **Repro:**
  1. At signup choose "Hybrid mesh".
  2. Open Settings; observe "Federated graph replication" ticked.
- **Fix:** Rename the Settings toggle so it does not reuse a workspace-type name, and show the chosen workspace type on the Settings page.

### fcc4878792e6 — Settings toggles Enable webhook sync and Vault attestation are unexplained engineering terms
- **Severity:** P2
- **So what:** A non-technical user cannot tell whether these protect or expose her notes, nicking trust on the settings page.
- **Framework tags:** A2
- **Flow:** shape_2b
- **Locator:** nav: Settings
- **Personas hit:** novice
- **Observed:**
  - Labels "Enable webhook sync", "Federated graph replication", "Vault attestation" with no helper text.
  - The one plain line on the page, "Export · Markdown, all cards", was understood immediately.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24`
  > ""Enable webhook sync", "Federated graph replication", "Vault attestation". No idea. There's an Export button — "Markdown, all cards". At least that's clear."
- **Repro:**
  1. Click "Settings" in the nav.
  2. Read the three checkbox labels.
- **Fix:** Add a one-line plain-language explanation under each toggle saying what it does to the user's notes.

### e6751066f311 — The same object is called a note, a card and a block across nav, dashboard and editor
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, slowing the first save.
- **Framework tags:** A4
- **Flow:** shape_1
- **Locator:** nav bar
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards", "New block"; dashboard: "Search your notes", "Your cards"; editor heading: "New block".
  - Settings export: "Markdown, all cards"; marketing promise and both personas say "notes".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Land on the dashboard; read the nav and the search placeholder.
  2. Click "New block"; read the heading.
- **Fix:** Pick one noun ("note" matches the users and the search box) and use it in the nav, dashboard heading, editor and export label.

### b82b3b5d133a — Empty dashboard says only Nothing here yet and gives no instruction for creating the first note
- **Severity:** P2
- **So what:** The activation moment is wasted; the novice expected her stuff and got no direction, then hunted the nav.
- **Framework tags:** A2, A10, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" with "Nothing here yet." — no button, link or hint.
  - Novice first tried search ("No results for 'meeting'."), then found "New block" in the nav at 01:40.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13`
  > "Dashboard. "Your cards" — "Nothing here yet." … Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a new workspace.
  2. Read the dashboard empty state.
- **Fix:** Make the empty state say how to write the first note, with a create button inside it.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "Saved ✓" toast wording on screen — `04-note-saved-toast.png` shows the empty editor, not the toast; wording rests on session.log only.
- Marketing-site copy beyond the one-line promise — the site was never captured.

## For other lenses
- Save does not persist and search returns nothing for saved titles — bugs.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) for a keyboard-driven persona — ux.
- Radio buttons and checkboxes render centred, detached from their labels, on signup and Settings — ux.
- Irreversible configuration before any value is shown — onboarding.

## Coverage gaps
- Marketing site that made the promise — not captured.
- Error copy for a failed save — never triggered visibly; product showed success instead.
- Export output — button seen, never clicked.
- Mobile viewport — both personas on desktop 1440×900.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 01 signup, 02 dashboard, 03 editor, 04 editor (toast not captured), 05 dashboard, 06 memories, 07 settings · power-user: 02 dashboard, 03 dashboard after search, 07 settings
