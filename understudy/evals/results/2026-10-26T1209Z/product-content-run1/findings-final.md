# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: promise-vs-delivery first, then Nielsen A2/A4/A9 (jargon, naming, error/empty copy) and Layer C
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on invented personas
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Layer B: applied only to Memories, the one surface presenting itself as machine-derived knowledge

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | Empty dashboard; two saved notes vanished; Memories listed three false facts | Fail | Gave up at 06:30; "No. Nothing, until saving works." |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Note lost after "Saved ✓"; search found nothing; no shortcuts; Memories "Not me" | Fail | Stopped at 03:00; would not switch the team; pay "Nothing." |

- Both Q4 answers agree with this reading: novice "No — it started completely empty"; power-user "It remembers nothing I gave it and claims things I didn't."
- The promise mismatch is the root cause of findings 2 and 3: the pitch is about remembering, and both failures are false claims about memory.

## Reading level and jargon
- Signup and Settings read at a technical-specialist level; Title/Body editor and "Markdown, all cards" read plainly.
- 6 jargon terms on 2 screens the novice met: "Federated graph", "Sovereign vault", "Hybrid mesh", "Enable webhook sync", "Federated graph replication", "Vault attestation".
- Novice could explain none of them: "I don't know what any of these are" (`persona-novice/session.log:10`).
- 3 names for one object: "Cards", "New block", "Search your notes".

---

## Findings

### 3fb5d3c39c0a — Product contradicts its own pitch: 'remembers everything' but starts empty and keeps nothing
- **Severity:** P0
- **So what:** Both personas arrived for memory and left calling the product the opposite; neither would return or pay.
- **Framework tags:** A2, B-G1, C-SOWHAT, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Pitch both personas carried in: "remembers everything so you never start from zero".
  - First screen after signup: "Your cards" — "Nothing here yet."; notes saved later never appear.
  - Both debriefs answer Q4 "No".
- **Evidence:** `persona-novice/session.log:2` · `persona-novice/session.log:12` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:2` · `persona-power-user/session.log:15` · `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
  > "No — it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine." (novice, Q4)
  > "\"Remembers everything.\" No. It remembers nothing I gave it and claims things I didn't." (power-user, Q4)
- **Repro:**
  1. Arrive with the marketing line "remembers everything so you never start from zero".
  2. Sign up; land on the dashboard.
  3. Write and save a note via "New block"; return to the dashboard.
- **Fix:** Pull "remembers everything" from the marketing site until saved notes reliably appear on the dashboard, or rewrite the pitch to what the app does today.

### 4e7b35e4c15f — Memories page states invented facts about the user as things Nimbus remembers
- **Severity:** P0
- **So what:** Confident nonsense about the user's own life made the novice doubt every other claim, including "Saved".
- **Framework tags:** A2, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/06-memories.png
- **Personas hit:** novice, power-user
- **Observed:**
  - Heading "What Nimbus remembers about you" over "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer: "Memories are built from your notes and connected accounts." — no notes persisted and no accounts connected in either session.
  - No label marks these as samples or demo data.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Sign up with a fresh workspace.
  2. Click "Memories" in the top menu.
  3. Read the three statements and the footer.
- **Fix:** Show an empty state on Memories until the user has real notes, or label sample content as "Example" and drop the "built from your notes" footer.

### 62d260d4df33 — 'Saved ✓' confirmation claims a save that the cards list and search never reflect
- **Severity:** P0
- **So what:** The novice concluded the product "is lying to me"; data appears lost, which ends trust in a notes app.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - "Saved ✓" toast after Save, three times across two personas.
  - Dashboard still reads "Nothing here yet."; search returns "No results for 'Dentist'" / no result for "Roadmap".
  - Toast never says where the note went or how to open it.
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
- **Repro:**
  1. Click "New block"; enter title "Dentist" and body text.
  2. Click "Save"; note the "Saved ✓" toast.
  3. Check the dashboard list and search "Dentist".
- **Fix:** Show "Saved ✓" only after the note is persisted, and link the toast to the saved note in the cards list.
- Severity note: torn between P0 and P1 for a copy finding; P0 chosen because the copy asserts a save the user cannot verify.

### 416e1dc60018 — Signup forces an irreversible workspace choice worded in jargon a novice cannot parse
- **Severity:** P2
- **So what:** The novice guessed at a permanent decision before seeing the product; a less patient user leaves here.
- **Framework tags:** A2, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** persona-novice/screenshots/01-signup-workspace-type.png
- **Personas hit:** novice
- **Observed:**
  - Options "Federated graph", "Sovereign vault", "Hybrid mesh" with no description.
  - Warning "This cannot be changed later." directly under them.
  - Novice spent 43 s (00:05–00:48) and picked by sound of the name.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "Picked "Hybrid mesh" because it sounds like it includes the other two."
- **Repro:**
  1. Clear the login wall; land on signup.
  2. Read "Before we begin, choose your workspace type".
- **Fix:** Add a one-line plain-language description under each workspace option stating what it changes for the user, or defer the choice until after first use.

### ef648037bdc0 — Settings toggles use engineering jargon with no explanation for a non-technical user
- **Severity:** P2
- **So what:** The novice could not act on 3 of 4 settings; only "Export" was usable, which erodes confidence in the product.
- **Framework tags:** A2, A10
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/07-settings.png
- **Personas hit:** novice
- **Observed:**
  - Toggles labelled "Enable webhook sync", "Federated graph replication" (on by default), "Vault attestation".
  - No helper text on any toggle.
  - "Export" with "Markdown, all cards" was the one control the novice understood.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24`
  > ""Enable webhook sync", "Federated graph replication", "Vault attestation". No idea. There's an Export button — "Markdown, all cards". At least that's clear."
- **Repro:**
  1. Click "Settings" in the top menu.
  2. Read the three toggle labels.
- **Fix:** Add a plain-language line under each Settings toggle saying what it does and who needs it; move developer toggles under an "Advanced" heading.

### 7527b136fd11 — Same item is called card, block and note across nav, editor and search
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, adding doubt at first use.
- **Framework tags:** A4, A2
- **Flow:** shape_2
- **Locator:** persona-novice/screenshots/02-dashboard-empty.png
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards", "New block"; dashboard heading "Your cards".
  - Search placeholder: "Search your notes"; editor heading "New block"; export "Markdown, all cards".
  - Marketing and both personas call the object a "note".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Land on the dashboard; read the nav, heading and search placeholder.
  2. Click "New block"; read the page heading.
- **Fix:** Pick one noun — "note" matches the pitch and the search box — and use it in the nav, dashboard heading, editor heading and export label.

### 5c0d0ad4b6bd — Empty dashboard says 'Nothing here yet.' with no pointer to writing a first note
- **Severity:** P2
- **So what:** The first screen gives no next step; the novice searched an empty workspace before finding "New block".
- **Framework tags:** A9, A6, C-TTFV
- **Flow:** shape_1
- **Locator:** persona-novice/screenshots/02-dashboard-empty.png
- **Personas hit:** novice
- **Observed:**
  - "Your cards" — "Nothing here yet." and nothing else in the panel.
  - Novice searched "meeting" (00:55–01:40) before trying the nav.
  - Search reply "No results for 'meeting'." also offers no next step.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14`
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Complete signup.
  2. Read the "Your cards" panel.
- **Fix:** Add to the "Your cards" empty state one line on how to start and a button to the new-note editor.

### 53ab7e3997cc — Workspace type name reappears as a settings toggle with no stated link between them
- **Severity:** P3
- **So what:** The power user could not tell if a default-on toggle was their signup choice; minor doubt, no behaviour change.
- **Framework tags:** A4
- **Flow:** shape_2b
- **Locator:** persona-power-user/screenshots/07-settings.png
- **Personas hit:** power-user
- **Observed:**
  - Signup option "Federated graph"; Settings toggle "Federated graph replication", checked by default.
  - No copy connects the two.
  - Power user accepted the signup jargon without complaint: "Fine — I've seen worse."
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:8` · `persona-power-user/session.log:13`
  > ""Federated graph replication" is on by default. I picked that at signup — is this the same thing?"
- **Repro:**
  1. Pick "Federated graph" at signup.
  2. Open "Settings"; read the second toggle.
- **Fix:** State on the Settings page which workspace type was chosen at signup, and say whether "Federated graph replication" depends on it.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "Saved ✓" toast wording — `persona-novice/screenshots/04-note-saved-toast.png` shows an empty New block form, not the toast; claim rests on session.log only.
- "No results for '…'" search copy — no screenshot shows the message; `persona-power-user/screenshots/03-search-empty.png` shows an empty search box.
- Marketing-site copy beyond the quoted line — never captured.

## For other lenses
- Notes not persisting after Save; search returning nothing — bugs.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) for the power user — ux.
- Irreversible choice before first value — onboarding.

## Coverage gaps
- Marketing site never captured; pitch known only from the pre-session line.
- Export never clicked; its output copy unread.
- No mobile device run.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice 00–07 opened; power-user 02, 03, 07 opened; novice 03 and 04 are identical empty editor frames
