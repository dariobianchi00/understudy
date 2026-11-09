# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Nielsen A-layer (A2 jargon, A4 naming, A9 error copy) + promise-vs-delivery (debrief Q4); Layer B where Memories makes AI-style claims
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | Empty dashboard; two notes lost after "Saved ✓"; Memories full of facts that are not hers | Fail | Gave up at 06:30; "I'd stop here"; would pay nothing |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Saved note vanished; search finds nothing; no shortcuts; invented Memories | Fail | Gave up at 03:00; "No. Nothing." |

- Both persona Q4 answers agree with this reading: novice "No — it started completely empty, it lost what I gave it"; power-user "It remembers nothing I gave it and claims things I didn't."
- The two P0s below are the mechanism of the promise failure: the product forgets what it was given and "remembers" what it was not.

## Copy sample — what the personas read

| Surface | Verbatim copy | Reading level vs persona | Jargon terms |
|---|---|---|---|
| Signup | "Before we begin, choose your workspace type" · "Federated graph" · "Sovereign vault" · "Hybrid mesh" · "This cannot be changed later." | Engineer/architect vocabulary; novice could not parse any option | 3 |
| Dashboard | "Search your notes" · "Your cards" · "Nothing here yet." | Plain, but names the object twice, differently | 0 (1 naming clash) |
| Editor | "New block" · "Title" · "Body" · "0 words" · "Preview below" · "Save" | Plain; the one surface the novice praised | 1 ("block") |
| Memories | "What Nimbus remembers about you" · "Memories are built from your notes and connected accounts." | Plain — the problem is truth, not difficulty | 0 |
| Settings | "Enable webhook sync" · "Federated graph replication" · "Vault attestation" · "Export" "Markdown, all cards" | Developer/infra vocabulary; no helper text on any toggle | 3 |

- Jargon density on first-session surfaces: 6 unexplained technical terms across 2 screens, 0 tooltips or helper lines.
- Clear copy exists: "Export" / "Markdown, all cards" was the only Settings item either persona understood.

---

## Findings

### eeb54e4ad2fd — "Saved ✓" confirmation reports notes that then vanish, contradicting "remembers everything"
- **Severity:** P0
- **So what:** The only confirmation copy in the product is false, so the novice concluded "It is lying to me" and stopped trusting every other message.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - After Save, a green "Saved ✓" appears; dashboard then still reads "Nothing here yet." and search returns "No results for 'Dentist'"
  - Novice repeated save twice with identical result; power-user once with "Roadmap"
  - No error copy ever says the save failed or what to do next
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-novice/persona-debrief.md`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  > "If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Sign up, open "New block", enter a title and body
  2. Click Save; observe "Saved ✓"
  3. Return to dashboard; observe "Nothing here yet."; search the title; observe "No results for '<title>'"
- **Fix:** Show "Saved ✓" only after the note is confirmed stored; on failure show an error saying the note was not saved and offering retry.

### ab197b468f31 — Memories page states invented facts as "What Nimbus remembers about you"
- **Severity:** P0
- **So what:** Confident claims about the user that are false turned the product's headline feature into proof it cannot be trusted, for both personas.
- **Framework tags:** A2, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/06-memories.png
- **Personas hit:** novice, power-user
- **Observed:**
  - Heading "What Nimbus remembers about you" over "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — no accounts connected, no note persisted
  - Nothing labels these as examples, and nothing lets the user correct or delete them
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from?"
  > "It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Create a new workspace with no connected accounts
  2. Click "Memories" in the top nav
  3. Observe three specific claims about the user and the "built from your notes and connected accounts" footer
- **Fix:** Show Memories only when derived from the user's own data, cite the source note for each, and label any sample content as a sample.

### dd4294d0355d — Blank "Nothing here yet." dashboard breaks the "never start from zero" promise and gives no next step
- **Severity:** P1
- **So what:** The novice arrived expecting her stuff pre-filled; the first screen is empty with no instruction, which she named in Q4 as the promise failure.
- **Framework tags:** A2, B-G1, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Dashboard shows "Your cards" and "Nothing here yet." — no action, link or explanation of how to add or import
  - Pre-session expectation: "a notes app that fills itself in from things I already have"
  - Severity flip: power-user expected an empty start ("Expected, nothing's in it yet") — non-issue for him
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:3` · `persona-novice/session.log:12` · `persona-novice/persona-debrief.md` · `persona-power-user/session.log:10`
  > "Nothing tells me what to do. I thought it would have my stuff."
  > "No — it started completely empty, it lost what I gave it"
- **Repro:**
  1. Arrive from the marketing promise "remembers everything so you never start from zero"
  2. Complete signup
  3. Observe the dashboard: "Nothing here yet." with no next step
- **Fix:** Make the dashboard empty state say how to create or import a first note, with a button, and align the marketing line with what a new account contains.

### 4d92837e6f7d — Signup forces an irreversible workspace choice in unexplained jargon
- **Severity:** P2
- **So what:** The novice guessed a permanent setting from names she could not parse; a less stubborn user leaves at second 20.
- **Framework tags:** A2, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Options "Federated graph", "Sovereign vault", "Hybrid mesh" with no description each
  - Warning "This cannot be changed later." precedes any view of the product
  - Novice picked "Hybrid mesh" "because it sounds like it includes the other two"; power-user shrugged ("Fine — I've seen worse")
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall; land on signup
  2. Read the three workspace options and the "cannot be changed later" line
- **Fix:** Give each workspace option a one-line plain-language consequence, or defer the choice until after first use and make it changeable.

### c82e75543069 — One object is called "cards", "block" and "notes" across nav, editor and search
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, adding a hunt before her first note.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** nav: Cards / New block / Search your notes
- **Personas hit:** novice
- **Observed:**
  - Nav "Cards" and "New block"; dashboard heading "Your cards"; search placeholder "Search your notes"
  - Editor heading "New block"; export label "Markdown, all cards"
  - Marketing and the persona both say "notes"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Open the dashboard; read the nav, the "Your cards" heading and the "Search your notes" placeholder
  2. Click "New block"; read the editor heading
- **Fix:** Pick one user-facing noun (the persona's word is "note") and use it in nav, headings, search placeholder and export label.

### 50bc54942e18 — Settings labels are unexplained infrastructure jargon, one reusing the signup term
- **Severity:** P2
- **So what:** Neither persona could tell what the toggles do, and the power-user could not tell if one changed his "permanent" signup choice.
- **Framework tags:** A2, A4, A10
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/07-settings.png
- **Personas hit:** novice, power-user
- **Observed:**
  - Toggles "Enable webhook sync", "Federated graph replication" (on by default), "Vault attestation" — no helper text
  - "Federated graph" also names a signup option the user was told "cannot be changed later"
  - "Export" / "Markdown, all cards" is the one label both understood
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-power-user/session.log:13`
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
  > "Webhook sync, graph replication, vault attestation — no idea. Export is clear."
- **Repro:**
  1. Open Settings
  2. Read the three toggle labels; compare "Federated graph replication" with the signup option "Federated graph"
- **Fix:** Add a one-line plain-language description under each Settings toggle, and either rename the replication toggle or link it to the workspace type.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast itself is not visible in `persona-novice/screenshots/04-note-saved-toast.png` — it shows an empty "New block" form; ID1 rests on session.log, not this screenshot.
- `persona-power-user/screenshots/03-search-empty.png` shows an empty search box and "Nothing here yet.", not the "No results for 'Roadmap'" message the log describes — wording of the no-results copy is log-only.
- Search no-results copy ("No results for '…'") may lack a next step — no screenshot captures it; not scored.

## For other lenses
- Save does not persist and search never returns the saved note — bugs
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux
- Signup radio buttons render centred, detached from their labels; same on Settings checkboxes — ux
- Irreversible decision before first use, empty first-run state — onboarding

## Coverage gaps
- Marketing site never captured; the promise is known only from the pre-session note
- Error states for a failed save never surfaced on screen, so no error copy could be read
- Export output never opened; "Markdown, all cards" not verified
- Desktop only (1440x900); no mobile copy layout

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index — novice 00–07 (no 04 toast visible); power-user 00, 02, 03, 07
