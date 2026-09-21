# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: promise-vs-delivery (debrief Q4) first, then Nielsen A2/A4/A9 on the copy each persona actually met
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED, not researched
- Scoring model: opus
- All 11 screenshots opened; every finding cites an artifact; unsupported observations listed at the end

---

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" | "Nothing here yet." on an empty dashboard; two notes accepted and lost; three "memories" belonging to someone else | **Fail** | Stopped at 06:30 with zero notes; Q1 answer is "right now: nothing"; would pay nothing |
| power-user | "remembers everything so you never start from zero" | Empty dashboard, no keyboard shortcuts, one note accepted and lost, search returns nothing | **Fail** | Stopped at 03:00; "Save doesn't save and search doesn't search"; would pay nothing |

- Both personas' own Q4 answers are **No**. My reading agrees with theirs — no disagreement to note.
- The promise is about *memory*. The product's only memory-shaped surface is the one that states things the persona never said. That is the root cause, not a separate defect.
- `manifest.json` has an empty `vocabulary_allowlist`, so no term below is sanctioned product vocabulary.

---

## Findings

### e5ea569f5a58 — Memories page presents three facts about the user that are not theirs and claims they came from their notes
- **Severity:** P0
- **So what:** Once the novice saw the product state things about her that were false, she stopped believing the "Saved ✓" confirmation too, and left.
- **Framework tags:** A2, A9, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** Memories page
- **Personas hit:** novice
- **Observed:**
  - Heading reads "What Nimbus remembers about you"; three statements follow, none supplied by the persona.
  - Footer copy asserts a source: "Memories are built from your notes and connected accounts." The persona had written one note, about a dentist, and connected no accounts.
  - No per-item provenance, no date, no "example" or "demo" label anywhere on the surface.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-novice/persona-debrief.md`
  > "You prefer to schedule meetings on Tuesday afternoons." · "Your team uses Jira and Slack." · "You are working on a product launch in Q4."
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
- **Repro:**
  1. Create a workspace and write one note.
  2. Open Memories from the top nav.
  3. Read the three statements and the footer line claiming they came from your notes.
- **Fix:** Show nothing on Memories until a memory has a real source, and label every item with the note or account it came from; delete the "built from your notes and connected accounts" line while it is untrue.

### 025e866d7ecd — Memories copy gives no provenance per item, so the power-user dismissed the whole surface as a demo
- **Severity:** P2
- **So what:** He kept using the product but classified a headline feature as filler, so the memory pitch earns nothing from him.
- **Framework tags:** A2, B-G2, B-G11
- **Flow:** shape_2b
- **Locator:** Memories page
- **Personas hit:** power-user
- **Observed:**
  - Same three statements; he recognised none of them as his.
  - He inferred an unstated status — "a demo panel" — because no copy states one.
  - He continued to Settings and the debrief rather than stopping here.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` · `persona-novice/screenshots/06-memories.png` (the wording, captured on the novice run)
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Open Memories on a workspace with no connected accounts.
  2. Look for any copy stating where an item came from or that it is sample content.
- **Fix:** Put the source under each memory ("from your note 'Roadmap', 8 Sep"), and if the list is seeded, say so in the panel rather than leaving the reader to guess.

### ff12f2fc5a92 — Entry promise "remembers everything so you never start from zero" appears nowhere in the product's own copy
- **Severity:** P1
- **So what:** Both personas answered "No" to whether the product matched its pitch, and neither could say in one sentence what it does for them.
- **Framework tags:** A2, B-G1, C-SOWHAT, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - First screen after signup says "Nothing here yet." — the literal opposite of "never start from zero".
  - No import, connect, or "bring your existing notes" copy anywhere in the three surfaces either persona reached.
  - The only copy that echoes the promise is the false provenance line on Memories.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-power-user/screenshots/02-dashboard.png` · `persona-novice/session.log:1-3,12` · `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
  > novice: "No — it started completely empty, it lost what I gave it, and the 'memories' it does have aren't mine."
  > power-user: "'Remembers everything.' No. It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Arrive from the marketing line "remembers everything so you never start from zero".
  2. Complete signup and read the dashboard.
  3. Look for any copy that explains how the product gets your existing material.
- **Fix:** On the empty dashboard, state in one line how Nimbus fills itself (import, connect, or "it starts with what you write"), so the first screen and the marketing line agree.

### 9d64aff72e8b — Failed save produces no error copy — "Saved ✓" and "Nothing here yet." are the only words offered
- **Severity:** P1
- **So what:** Both personas abandoned the objective under test with no wording anywhere telling them what happened or what to do next.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save produces a green "Saved ✓" toast; the dashboard then shows "Nothing here yet."
  - The novice saved twice and got the identical confirmation both times, with no second message contradicting it.
  - No error text, warning, or retry wording appears on either surface; console is clean.
- **Evidence:** `persona-novice/session.log:17-20` · `persona-power-user/session.log:11` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/console-full.txt`
  > novice: "Wrote it again, saved again, 'Saved ✓' again, dashboard empty again. It is lying to me."
- **Repro:**
  1. Open New block, enter a title and body, click Save.
  2. Read the toast, then read the dashboard.
  3. Look for any copy explaining the discrepancy.
- **Fix:** Make the confirmation copy conditional on the write actually succeeding, and add a plain-language failure message on `/app/new.html` naming what to do with the text still in the box.

### 64e1f43e1cbb — Signup demands an irreversible choice between three undefined terms with no explanatory copy
- **Severity:** P2
- **So what:** The novice made an undoable configuration decision by guessing at a word, 48 seconds into the product.
- **Framework tags:** A2, A5, B-G1
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Three radio options — "Federated graph", "Sovereign vault", "Hybrid mesh" — with no description, tooltip, or default.
  - Subtext reads "This cannot be changed later."; heading is "Before we begin, choose your workspace type".
  - The persona chose on the sound of the word, not its meaning.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9-11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
  > "Picked 'Hybrid mesh' because it sounds like it includes the other two."
- **Repro:**
  1. Clear the login wall and land on `/app/signup.html`.
  2. Read the three option labels and look for any explanation of the difference.
- **Fix:** Add one plain sentence under each workspace-type option saying what it means for the user's notes, and mark a recommended default.

### f2bc73a1a399 — One concept is named three ways — "Cards", "New block", "Search your notes"
- **Severity:** P2
- **So what:** The novice could not tell whether "New block" would produce the thing that "Cards" lists, so she did not know where her note had gone.
- **Framework tags:** A2, A4, A6
- **Flow:** shape_1
- **Locator:** Global nav
- **Personas hit:** novice
- **Observed:**
  - Top nav reads "Cards" and "New block"; the dashboard heading is "Your cards"; the search placeholder is "Search your notes".
  - The editor page title is "New block"; the Settings export caption is "Markdown, all cards".
  - The persona asked which of the three was the same thing before clicking anything.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Read the top nav, the dashboard heading, the search placeholder and the editor title in sequence.
  2. Count the words used for a single saved item.
- **Fix:** Pick one noun for the unit — note, card, or block — and use it in the nav, the dashboard heading, the search placeholder, the editor title and the export caption.

### db818865c631 — Settings labels three toggles in internal jargon with no explanatory copy
- **Severity:** P2
- **So what:** The novice left Settings unable to say what any of the three switches would do to her notes, and trusted the product a little less for it.
- **Framework tags:** A2, A10
- **Flow:** shape_2b
- **Locator:** Settings page
- **Personas hit:** novice
- **Observed:**
  - Labels are "Enable webhook sync", "Federated graph replication", "Vault attestation" — no helper text under any of them.
  - "Federated graph replication" is checked on by default; the other two are off. No copy says what being on means.
  - The one control the persona understood carries a caption: "Export" with "Markdown, all cards".
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23-24`
  > "'Enable webhook sync', 'Federated graph replication', 'Vault attestation'. No idea. There's an Export button — 'Markdown, all cards'. At least that's clear."
- **Repro:**
  1. Open Settings.
  2. Read the three toggle labels and look for helper text.
- **Fix:** Give each Settings toggle a one-line caption in the same plain register as "Markdown, all cards", saying what it does to the user's notes.

### 1bb1ddb1e9da — "Federated graph" names both a signup workspace type and a Settings toggle with no stated link
- **Severity:** P2
- **So what:** The power-user could not tell whether the checked toggle was the irreversible choice he made at signup or a separate switch he could break.
- **Framework tags:** A4, A6
- **Flow:** shape_2b
- **Locator:** Settings page
- **Personas hit:** power-user
- **Observed:**
  - He selected "Federated graph" as his workspace type at signup.
  - Settings shows "Federated graph replication", checked, with no reference back to the workspace type.
  - He raised the ambiguity and moved on without resolving it.
- **Evidence:** `persona-power-user/session.log:8,13` · `persona-power-user/screenshots/07-settings.png` · `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-power-user/findings-raw.json`
  > "'Federated graph replication' is on by default. I picked that at signup — is this the same thing?"
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Pick "Federated graph" at signup.
  2. Open Settings and read "Federated graph replication".
  3. Look for any copy relating the two.
- **Fix:** Either rename the Settings toggle so it cannot be read as the workspace type, or state the relationship on the toggle ("your workspace type — set at signup, cannot be changed").

### 6ad9c88a9947 — Dashboard empty state "Nothing here yet." names no next action
- **Severity:** P2
- **So what:** The novice's first screen after signup told her the workspace was empty and nothing else, so she spent 45 seconds hunting for how to start.
- **Framework tags:** A2, A6, B-G1, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Empty state is a single grey line, "Nothing here yet.", under the heading "Your cards".
  - No call to action, no link to "New block", no explanation of what a card is.
  - She tried the search box first, then read the nav, before finding the editor at 01:40.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12-14` · `persona-novice/findings-raw.json`
  > "Dashboard. 'Your cards' — 'Nothing here yet.' Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Complete signup.
  2. Read the dashboard empty state and look for a next step.
- **Fix:** Replace the empty-state line on `/app/dashboard.html` with a sentence naming the action and linking to the editor.

### 08883f2f4d5b — Zero-result copy is identical whether the workspace is empty or a saved note is missing
- **Severity:** P2
- **So what:** Both personas searched for a title they had just saved, got the same message they had got on an empty workspace, and could not tell a miss from a malfunction.
- **Framework tags:** A1, A9
- **Flow:** shape_2
- **Locator:** /app/dashboard.html search box
- **Personas hit:** novice, power-user
- **Observed:**
  - The novice got "No results for 'meeting'." on an empty workspace, then "No results for 'Dentist'." after saving a note titled Dentist.
  - The power-user got "No results for 'test'." before saving and no results for "Roadmap" after saving.
  - The message offers no next step and no statement of how many notes were searched.
- **Evidence:** `persona-novice/session.log:13,19` · `persona-power-user/session.log:10-11` · `persona-power-user/screenshots/03-search-empty.png`
  > novice: "Typed 'Dentist' in search. 'No results for 'Dentist'.' It said saved."
  > power-user: "Save doesn't save and search doesn't search."
- **Repro:**
  1. Search any term on a new workspace and read the message.
  2. Save a note, search its exact title, and compare the two messages.
- **Fix:** Make the zero-result copy state how many notes were searched and offer a next step, so an empty workspace and a failed lookup read differently.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Reading level of the signup and Settings copy cannot be estimated properly — the screens carry 3–6 word labels and no sentences, so a grade-level measure would be noise. The jargon count is reported instead.
- No copy was seen for a populated card list, a note-detail view, or any server error; neither persona reached those surfaces, so their wording is unscored.
- Whether "Memories" is seeded demo content or a genuine inference is unknown — no copy states either, and nothing in the artifacts settles it. Scored only as the copy failure, not as fabrication.

## For other lenses
- Notes are accepted and never persisted; search never returns a saved note — `bugs`.
- The irreversible workspace-type decision is demanded before any value is shown — `ux`.
- No keyboard shortcuts at all (Ctrl+K, Ctrl+N, `/` all inert) for the power-user — `ux`.
- The novice reached a small first value at 02:41 (live word count and preview) and lost it again; the power-user never did — `onboarding`.

## Coverage gaps
- `persona-novice/screenshots/04-note-saved-toast.png` is byte-for-byte the same view as `03-new-note.png` — an empty form, no toast. The "Saved ✓" wording is evidenced by `session.log:17,20` only; the toast's exact rendering was never captured.
- No Memories screenshot exists for the power-user run; `findings-raw.json` attributes that reaction to `02-dashboard.png`. The wording is quoted from the novice capture.
- No zero-result screenshot exists on either run — `03-search-empty.png` shows the dashboard empty state, not the "No results for …" message.
- Mobile and tablet viewports never tested; both personas ran desktop-1440x900.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index — 8 novice captures (`00-start`, `00-wall-cleared`, `01`–`07`), 4 power-user captures (`00-start`, `02-dashboard`, `03-search-empty`, `07-settings`)
