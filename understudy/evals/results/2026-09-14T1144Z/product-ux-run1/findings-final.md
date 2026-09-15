# Nimbus Notes — ux findings — Run 2026-09-14 (fixture02)

## Method
- Framework: Nielsen A1–A10 · HAX B-G1/G2/G11 (the "Memories" panel is a user-facing inference surface, so Layer B applies) · Layer C activation
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — **INFERRED**, not researched; findings rest on personas the harness invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- All 12 screenshots opened; `04-note-saved-toast.png` does **not** contain the toast it is named for, so the toast is cited from `session.log` only

---

## Findings

### 064fc3e9c710 — Save confirms success but the note never appears in the card list or in search
- **Severity:** P0
- **So what:** Both personas believe the product destroyed their note, and both quit inside seven minutes without paying.
- **Framework tags:** A1, A9, C-TTFV, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save returns a green "Saved ✓", then the dashboard still reads "Nothing here yet."
  - Searching the note's own title returns "No results for 'Dentist'" / "No results for 'Roadmap'".
  - The novice repeated the whole write-and-save cycle a second time; identical result.
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/timeline.json`
  > "Saved twice, empty twice. It is lying to me."
  > "Nothing yet — it accepts a note and then loses it."
- **Repro:**
  1. Open **New block**, enter a title and body.
  2. Click **Save** and read the "Saved ✓" toast.
  3. Land on the dashboard — "Your cards" still reads "Nothing here yet."
  4. Search the note's title — "No results for '<title>'".
- **Fix:** Do not show "Saved ✓" until the write is confirmed; on failure show "Couldn't save — retry" with the draft still in the editor, and make the saved card render in "Your cards" and in search.

### fc93ce6d3aa3-a — Memories asserts three facts the user never entered as things Nimbus "remembers about you"
- **Severity:** P0
- **So what:** The novice concluded the product invents things, and immediately doubted the one confirmation it had given her.
- **Framework tags:** B-G1, B-G2, B-G11, A1, C-ABANDON
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/06-memories.png
- **Personas hit:** novice
- **Observed:**
  - Under "What Nimbus remembers about you": "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - The persona's entire input was one note titled "Dentist"; no account was ever connected.
  - The only explanation offered is the footnote "Memories are built from your notes and connected accounts." — which is untrue here and names no source per item.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
- **Repro:**
  1. Create a workspace and write exactly one note.
  2. Open **Memories** from the top nav.
  3. Read three first-person assertions about a user who supplied none of them.
- **Fix:** Show no memory the account has not actually produced — render an empty state instead — and attach a "from: <note or account>" source line to every memory that does appear.

### fc93ce6d3aa3-b — Memories asserts three facts the user never entered as things Nimbus "remembers about you"
- **Severity:** P2
- **So what:** The power-user wrote the whole surface off as fake demo content, so a headline feature scored zero with him rather than negative.
- **Framework tags:** B-G1, B-G2, A8
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/06-memories.png
- **Personas hit:** power-user
- **Observed:**
  - Same three assertions; the power-user read them as seeded demo data rather than a claim about him.
  - He did not try to correct, dismiss or delete any of them — no affordance to do so is visible on the panel.
  - He still cited it in the debrief as evidence the product's promise is false.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` · `persona-power-user/persona-debrief.md`
  > "Memories aren't mine. A demo panel, I assume."
  > "It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Create a workspace, save one note, open **Memories**.
  2. Note there is no control to dismiss, edit or dispute any memory.
- **Fix:** Label seeded examples as examples, and give every memory an inline dismiss/correct control on the Memories panel.

### 22991ce512b8 — Empty start with no import path contradicts the "never start from zero" promise both personas arrived on
- **Severity:** P1
- **So what:** Both personas expected their existing material to be there and found nothing, so the product's core claim failed within a minute.
- **Framework tags:** B-G1, A1, C-TTFV, C-SOWHAT
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Both arrived on "remembers everything so you never start from zero"; the first screen after signup is an empty card list.
  - No connect, import or sync affordance appears anywhere in the nav — only Cards, New block, Memories, Settings.
  - The Memories footnote references "connected accounts", but no route to connect one was found.
- **Evidence:** `persona-novice/session.log:2` · `persona-novice/session.log:12` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/06-memories.png` · `persona-power-user/persona-debrief.md`
  > "I thought it would have my stuff."
  > "No — it started completely empty, it lost what I gave it, and the 'memories' it does have aren't mine."
- **Repro:**
  1. Complete signup.
  2. Land on the dashboard and look for any way to bring in existing notes or accounts.
- **Fix:** Put a "Connect an account / import notes" action on the empty dashboard, or drop "never start from zero" from the acquisition copy.

### d89ead09e429 — Signup demands an irreversible choice between three undefined workspace types before the product is seen
- **Severity:** P1
- **So what:** The novice spent 43 seconds guessing at a decision she was told she could never undo, before seeing a single feature.
- **Framework tags:** A2, A3, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type" offers "Federated graph", "Sovereign vault", "Hybrid mesh" with no description of any of them.
  - Sub-label reads "This cannot be changed later."; there is no Skip, Back or "decide later".
  - She chose "Hybrid mesh" on the guess that it "sounds like it includes the other two".
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall and land on the workspace-type step.
  2. Try to learn what any of the three options means, or to defer the choice.
- **Fix:** Default new workspaces to one option, move the choice into Settings as changeable, and give each option a one-line plain-English description.

### 3e2a65a93d9c — Empty dashboard says "Nothing here yet." and offers no way to start
- **Severity:** P2
- **So what:** The first screen after signup gives the novice no next step, so the route to a first note is a hunt.
- **Framework tags:** A6, A1, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel contains the single line "Nothing here yet." — no button, no example, no hint.
  - The only route to writing is the "New block" item in the top nav, unlabelled as the primary action.
  - She first tried the search box, searching "meeting" against an empty account.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/findings-raw.json`
  > "'Nothing here yet.' Nothing tells me what to do."
- **Repro:**
  1. Complete signup and land on the dashboard.
  2. Look for a primary action in the "Your cards" empty state.
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button that opens the editor.

### 482d5fa7620c — One object is called cards, blocks and notes across four surfaces
- **Severity:** P2
- **So what:** The novice could not tell whether "New block" would produce the thing "Your cards" was waiting for, and had to guess.
- **Framework tags:** A2, A4
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Same object, four labels on three screens: nav "Cards" / "New block", heading "Your cards", search placeholder "Search your notes", export note "Markdown, all cards".
  - The naming stall cost a navigation hunt before she reached the editor.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Cards and blocks — same thing?"
- **Repro:**
  1. Read the dashboard heading, the search placeholder and the nav items in one pass.
  2. Compare with the "New block" editor title and the Settings export label.
- **Fix:** Pick one noun — "note" — and use it in the nav, the dashboard heading, the editor title, the search placeholder and the export label.

### 833518edf8b9 — Settings shows "Federated graph replication" on for a user who chose "Hybrid mesh" at signup
- **Severity:** P2
- **So what:** The one irreversible decision the product forced has no traceable effect, so neither persona can tell what they actually chose.
- **Framework tags:** A1, A4, A3
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/07-settings.png
- **Personas hit:** novice, power-user
- **Observed:**
  - The novice selected "Hybrid mesh"; her Settings screen shows "Federated graph replication" checked and the other two unchecked.
  - The power-user selected "Federated graph" and saw an identical screen — the same state for two different choices.
  - Nothing on Settings names the workspace type that was chosen, or links back to it.
- **Evidence:** `persona-novice/session.log:11` · `persona-novice/screenshots/07-settings.png` · `persona-power-user/session.log:8` · `persona-power-user/session.log:13` · `persona-power-user/screenshots/07-settings.png`
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Choose "Hybrid mesh" at signup.
  2. Open **Settings** and read the "Federated graph replication" checkbox state.
- **Fix:** Show the chosen workspace type as a read-only line at the top of Settings, and derive the replication toggle's default from it.

### 8d4902350090 — Settings toggles are labelled in infrastructure terms the persona cannot decode
- **Severity:** P2
- **So what:** The novice cannot judge whether any setting affects her data, so she leaves defaults she does not understand in place.
- **Framework tags:** A2, A6
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/07-settings.png
- **Personas hit:** novice
- **Observed:**
  - Three checkboxes, no help text: "Enable webhook sync", "Federated graph replication", "Vault attestation".
  - One is on by default and none states a consequence.
  - The one control she did understand was the "Export" button, captioned "Markdown, all cards".
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24`
  > "'Enable webhook sync', 'Federated graph replication', 'Vault attestation'. No idea. There's an Export button — 'Markdown, all cards'. At least that's clear."
- **Repro:**
  1. Open **Settings**.
  2. Attempt to decide whether to change any of the three toggles from the label alone.
- **Fix:** Give each toggle a one-line plain-English consequence beneath it, and move developer-only options behind an "Advanced" disclosure.

### 2ebc1989bcf1 — No keyboard shortcut reaches new note or search
- **Severity:** P2
- **So what:** The power-user came to evaluate fast keyboard capture and found none, removing his main reason to switch.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - Ctrl+K, Ctrl+N and `/` all did nothing from the dashboard.
  - No shortcut hint appears in the nav, the search field or the editor.
- **Evidence:** `persona-power-user/session.log:3` · `persona-power-user/session.log:12` · `persona-power-user/screenshots/02-dashboard.png` · `persona-power-user/findings-raw.json`
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Land on the dashboard.
  2. Press Ctrl+K, then Ctrl+N, then `/`.
- **Fix:** Bind `/` and Ctrl+K to the search field and Ctrl+N to New block, and show the hint inside the search placeholder.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast may not be dismissible or announced — `04-note-saved-toast.png` shows the empty editor, not the toast; no capture of the toast exists.
- Whether the note survives a page reload or exists anywhere — neither persona reloaded or used Export to check.
- Whether "Cards" in the nav leads anywhere other than the dashboard — never clicked by either persona.
- Whether search matches body text as well as titles — only titles were searched.
- Mobile and tablet behaviour — both personas ran desktop 1440x900 only.

## For other lenses
- The save endpoint's actual behaviour and any console/network failure behind the false "Saved ✓" — `bugs`.
- Density of infrastructure jargon in signup and Settings copy as a copy-quality question — `content`.
- Both personas abandoning before the single objective completed, as a funnel result — `onboarding`.
- Accessibility of the unlabelled radio/checkbox groups on signup and Settings — no lens covers WCAG in this harness; not scored here.

## Coverage gaps
- "Cards" nav destination never opened by either persona.
- Export never clicked, so the "Markdown, all cards" output was never seen.
- No note ever edited or deleted — undo/delete paths untested.
- Mobile and tablet viewports never tested.
- Login and account-recovery flows excluded by scope (auth wall).

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — `persona-novice/screenshots/` (8) · `persona-power-user/screenshots/` (4)
