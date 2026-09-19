# understudy

**An agent that stands in for a user, drives a live web product, and reports back through a chosen lens.**

You give it a product, a persona and a question. It signs up, gets stuck where a real person would get stuck, gives up if a real person would give up — then hands you a severity-rated report where every finding cites a screenshot.

The trick is that **one traversal answers many questions.** *Is the UX any good? · What's broken? · Where do people drop off? · Does it deliver what the marketing promised?* — four reports, one browser session, because they all score the same evidence.

It does the same for websites: a visitor with a question lands, orients, evaluates and decides, and `clarity`, `conversion` and `trust` all score that one visit.

```
/plugin marketplace add dariobianchi00/understudy
/plugin install understudy
/understudy:run
```

> **v0.7.2 — profiles get a real illustration.** The face on each ICP card is an illustrated portrait (Open Peeps by Pablo Stanley, CC BY 4.0, via DiceBear), fetched once per profile at render time and cached in `icp/avatars/` so re-renders are offline; when the first render has no network, the drawn silhouette stands in. Each profile starts on its own page in the PDF.
>
> **v0.7.1 — Ideal Customer Profiles as people.** Each profile is now a card in both the PDF and the interactive report: a drawn face (a deterministic SVG, never a photo, never a real person), a name and one line of life from the lens's new `Meet:` field, the *Who* sentence, then the job, trigger, where to find fifty, why it wins, what it lacks, fit and propensity as bars, the case against, and the re-run persona. No screenshots in this section — a profile is an inference, and thumbnails dressed it as an observation. `scripts/icp_profiles.py` parses and renders; a profile without a `Meet:` line gets a placeholder name and says so.
>
> **v0.7.0 — the interactive report.** `--format html` is now a presentation instrument, not the PDF in a browser: a dashboard over the run (score rings, Top 5, persona cards), a findings explorer with filters and a detail drawer, a session replay per persona with the screen that was showing at each log line, the ICP profiles, a full-screen Present mode, a lightbox, and triage with export. One self-contained file, branded with the site's own icon and accent. The template is `scripts/report_template.html`; `scripts/interactive_report.py` packs a run into it. The printed PDF is unchanged.
>
> **v0.6.4 — the report reads better.** The cover carries the site's own icon (fetched once, cached as `site-logo.<ext>` in the run folder, silently absent offline). The *Where* column of *In their own words* is usable: each screenshot is a thumbnail that opens the file, each log or debrief citation is a short link to it, and *Top 5 row N* jumps to the table. The *Why that score* column is sentence-cased with a full stop, whatever the lens wrote.
>
> **v0.6.3 — quotes with prices.** `check_report.py` now decodes `findings-raw.json` before matching *In their own words* rows; it read the file as text, so `json.dump`'s `\u20ac` escape meant any quote containing a currency sign failed the gate. Found on the first *both* run (a hotel site, three personas, six captures).
>
> **v0.6.2 — in their own words.** The run summary gains a section of verbatim lines from the personas — what they said at the moment behind each top finding, with the log line beside it. The gate checks every quote against the persona files and fails a quote the log does not contain; an improved quotation is fabricated evidence in the one section a reader repeats out loud.
>
> **v0.6.1 — scores from what the personas did.** A P1 now needs an observed moment (a persona stopped, left, failed, or said they would not pay or return); a complaint with continued use is a P2. The 0–10 bands carry a "looks like" column, the lens scores from the personas' outcome first and checks the severity ceiling second, and the gate prints a note when a verdict says everyone got value above a score that says a meaningful share gave up. The ceilings themselves are unchanged.
>
> **v0.6.0 — who is this for?** A twelfth lens, `icp`, derives three ideal customer profiles from the captured evidence — primary, expansion, next-best — each scored on fit and propensity, each carrying the case against it and a persona for a re-run, with the trap segment named. No market research: the product is the world. See *The lenses*.
>
> **v0.5.3 — the status line goes quiet.** The one-line status at the bottom of Claude Code clears itself an hour after a run finishes, instead of showing that run forever.
>
> **v0.5.2 — watch it run, with nothing to type.** A run asks "open the live view?" and a yes opens a window on it: who is doing what, the persona's commentary as it is written, the auth pause, every screenshot as it lands. `/understudy:watch` opens it later and sets up the one-line status at the bottom of Claude Code on a yes. See *Watching it run*.
>
> **v0.4.1 — one row per problem.** The summary export names each problem once, with every check's own severity beside it, and corroboration pairs on evidence rather than on product vocabulary.
>
> **v0.4.0 — evaluated, not just built.** Product and website assessment run end to end — interview → capture → the lenses → verified report → PDF or HTML. The harness now grades itself: a frozen fictional site with planted defects, weekly lens and behaviour evals, and a ×3 baseline (30 runs, 30 gates passed, 0 hallucinations) that every later run is measured against. What it will not do, it says so rather than approximating.

---

## Contents

- [Why it works this way](#why-it-works-this-way)
- [Install](#install) · [Prerequisite](#prerequisite--playwright-mcp)
- [Your first run](#your-first-run)
- [The lenses](#the-lenses) · [Adding one](#adding-a-lens)
- [Coverage depth](#coverage-depth--how-much-gets-opened)
- [Watching it run](#watching-it-run)
- [What a run produces](#what-a-run-produces)
- [Models — you choose, at both levels](#models--you-choose-at-both-levels)
- [Personas — read before trusting a report](#personas--read-this-before-trusting-a-report)
- [Credentials and data](#this-tool-never-stores-your-credentials-or-your-product-data)
- [How it verifies itself](#how-it-verifies-itself)

---

## Why it works this way

Three design decisions do most of the work. They are worth two minutes because they explain what the output is and isn't.

### 1. The persona never sees the framework

Evaluation happens in two passes. **Pass 1** is a persona with a goal and a short attention span who has never heard of a usability heuristic. **Pass 2** is an analyst who reads what they left behind and scores it.

The persona's confusion is uncontaminated data — they weren't looking for problems, so what tripped them is real. An agent that knows the framework goes looking for framework-shaped problems and finds them, every time, producing a report that confirms its own priors while looking exactly like evidence.

Scoring vocabulary is **banned** during capture and **checked mechanically** afterwards. One hit fails the run.

### 2. Objectives group by evidence, not by topic

The natural instinct is to group by subject. The useful grouping is *what the agent physically has to do to gather the evidence*:

| Mode | Evidence gathering | Lenses |
|---|---|---|
| **A — Journey** | A persona with a goal drives the product. One traversal, many scorings. | `ux` `bugs` `onboarding` `content` `icp` |
| **A-visit — Visit** | A persona with a *question* reads a site. Same machinery, different flow shapes, a quarter of the time. | `clarity` `conversion` `trust` `icp` |
| **B — Instrumented** | Scripted and measured. No persona. | `technical` |
| **C — Crawl** | No session, no login. | `seo` `aeo` |
| **D — Comparative** | N runs of A-visit or C, then a diff pass. | `compare` |

The contract: **group objectives by mode → capture once per mode → fan out every scoring for that mode.** Four Mode-A lenses cost *one* traversal. Running an agent per objective would cost 4× for identical evidence.

**A-visit is a variant of A, not a separate mode.** The evidence-gathering is identical; only the flow shapes differ, so it reuses the capture gate, the evidence rules and the two-pass separation unchanged. But the shapes matter: a product user's journey is *entry → activation → first value*, while a visitor's is **land → orient → evaluate → decide**, and their "first value" is *"did I understand what this is and decide whether to care?"* — reached in twenty seconds or never. Push a visitor through product shapes and you get findings about a signup flow they were never going to reach.

### 3. Every finding cites evidence, with no exceptions

No screenshot, log line or DOM excerpt → the finding is dropped. This holds **especially** for findings that are obviously true, because the obviously-true finding is the one nobody checks and the one a model is most likely to have confabulated about a screen it never opened.

Findings that don't make it appear in a **"Dropped for want of evidence"** list — which is what makes the rule cheap to obey instead of something to smuggle findings past.

---

## Install

```
/plugin marketplace add dariobianchi00/understudy
/plugin install understudy
```

### Prerequisite — Playwright MCP

understudy drives a **real browser** through the Playwright MCP server. Without it, traversal cannot run, and `/understudy:run` stops at pre-flight rather than pretending otherwise.

```
claude mcp add playwright npx @playwright/mcp@latest
```

Restart Claude Code afterwards.

<details>
<summary><b>Two version-dependent quirks — <code>browser_resize</code> and where screenshots land</b></summary>

Both are upstream Playwright-MCP behaviour, not understudy bugs, and both vary by
version. understudy handles them automatically; they are documented so a line in
a log makes sense rather than looking like a failure.

**`browser_resize`.** Some versions reject numeric arguments. Recent ones accept
them and simply call `setViewportSize` internally — as of 2026-09-04 the direct
call works and no workaround is needed. Where it does fail, understudy sets the
viewport directly:

```js
await page.setViewportSize({ width: W, height: H })
```

via the server's run-code tool (named `browser_run_code` or
`browser_run_code_unsafe` depending on version).

**Either way, understudy verifies the result** with `browser_evaluate` →
`window.innerWidth`, and this is the part that actually matters. A persona
defined by their device is silently testing the wrong product if the viewport
stayed at the default, and the screenshots just look like a slightly different
layout. The check is cheap and runs every time regardless of which path set the
viewport.

**Screenshots cannot be written straight into your run folder.** The MCP server
confines file writes to its own output roots — typically the directory Claude
Code was started in, plus `.playwright-mcp/` beneath it. Passing an absolute
path under `~/.understudy/runs/` is refused:

```
Error: File access denied: … is outside allowed roots.
```

So understudy captures each screenshot with a plain filename and **moves it into
the persona's run folder immediately afterwards.** Nothing real is left behind:
the repo's `.gitignore` covers `*.png` and `.playwright-mcp/` precisely because
this transit is unavoidable, and the traversal cleans up after itself. If you
ever find stray `NN-*.png` files in your working directory, a traversal was
interrupted mid-capture — they are safe to delete, and the run folder is the
authoritative copy.
</details>

---

## Your first run

```
/understudy:run
```

It interviews you — one question at a time, never assuming — then echoes a plan and waits for you to say go.

```
RUN PLAN — Acme Notes
─────────────────────────────────────────────────────
Target        acme-notes  ·  https://acme.example
Auth          wall at /login, human-in-the-loop pause

Objectives    Mode A → ux, bugs, onboarding, content

Personas      3, INFERRED (generic)        ← flagged in the report
              novice        desktop-1440x900
              power-user    desktop-1440x900
              sceptic       iphone-13

Captures      3 × Mode-A traversal  (90 min cap each)
Scoring       4 lenses over the same evidence, in parallel

Models        traversal   <session model>  (session-set; I can't change it)
              scoring     balanced

Excluded      Identity proxy — infrastructure, not a defect
Deliverable   executive summary · PDF
Run folder    ./understudy-runs/acme-notes/   (gitignored)

Estimated     ~4.5h traversal + ~1h scoring
─────────────────────────────────────────────────────
Go?
```

Note **Captures vs Scoring**: three traversals, four lenses. Adding `content` doesn't add a traversal.

**Time is quoted before you commit, not after** — three personas at 90 minutes is most of a working day, and that should never be a surprise at hour four.

### At an auth wall

```
→ [novice] traversal — auth wall detected at /login
⏸  PAUSED — authenticate in the open browser, then confirm
→ [novice] traversal — resuming at /dashboard
```

You log in. understudy never sees the credential, and the persona never drives an identity provider's UI. **The wall is never reported as a finding** — it's infrastructure.

### Later

```
/understudy:report ~/.understudy/runs/acme-notes/2026-09-04-run-a1b2c3d4 --lens content
```

Adds a lens to a finished run. No browser opens; it re-reads the evidence.

---

## The lenses

understudy answers two different questions, and asks you which one first.

### Product assessment — something people sign into and use

| Lens | Asks | Output | Mode | Model |
|---|---|---|---|---|
| `ux` | Is this usable? | Nielsen 10 + HAX + activation, severity-rated | A | opus |
| `bugs` | What's broken? | Repro steps + environment — a bug report, not a findings list | A | sonnet |
| `onboarding` | Where do people drop off? | A funnel — steps to value, time to value, drop-off points | A | opus |
| `content` | Does it deliver what it promised? | Promise-vs-delivery, reading level, jargon density | A | opus |
| `icp` | Who should this be built and sold for? | Three ideal customer profiles from the evidence — see below | A / A-visit | opus |

### Website assessment — something people read and decide from

| Lens | Asks | Output | Mode | Model |
|---|---|---|---|---|
| `clarity` | Can a visitor tell what this is? | Time-to-comprehension, what they misunderstood | A-visit | opus |
| `conversion` | Is the next step obvious? | CTA hierarchy, form burden, dead ends — against *your* stated goal | A-visit | opus |
| `trust` | Would they believe it? | Proof, pricing transparency, provenance, data handling | A-visit | opus |
| `icp` | Who should this be built and sold for? | Three ideal customer profiles from the site's words, pricing and proof — see below | A-visit / A | opus |
| `technical` | What does it cost to load? | Core Web Vitals, weight, image hygiene — **lab numbers, mobile and desktop separately** | B | sonnet |
| `seo` | Can it be found? | Crawlability, meta, canonical, structured data, sitemap | C | sonnet |
| `aeo` | Can it be answered *from*? | schema.org, answer blocks, entity clarity, `llms.txt` — **static markup only** | C | sonnet |
| `compare` | How does it stack up? | Differences matrix across your site and competitors *you* name | D | opus |

**Adding a lens inside a mode you are already running is nearly free** — it scores evidence already captured. Adding a *mode* means another pass through the site. `clarity + conversion + trust` is one visit; `clarity + seo` is two captures.

### `icp` — who this should be built and sold for

Most lenses ask whether the product works. `icp` asks **who it works for**, on the evidence of what it is. It reads the captured visit and journey — the site's own words, its proof, its pricing, the flows the product actually has — and returns three **ideal customer profiles**: a primary, an expansion bet and a next-best, each specific enough to find fifty of them, and each arguing with itself.

Per profile: who they are and where to find them · the job they are hiring the product for · the trigger that makes them look · why this product wins for them and what it lacks, every line citing a screenshot or a persona's words · a **fit** score (pain, alignment, evidence, clarity) and a **propensity** score (reach, trigger, willingness to pay, openness to switching), each 1–5 · **the case against** — what they use instead, the switching cost, the one fact that would kill the profile, and the cheapest one-week test · what the run could not tell · and a **persona in the target-file shape**, so the next run can put the product in front of exactly this customer. It also names the **trap**: the segment that is easy to sell to and would churn.

Two things it deliberately does not do. It does **no market research** — no web search, no reviews, no competitor pages; the product is the world, and where the evidence does not reach the profile says *not inferable* rather than guessing. And it never pads: if fewer than three segments clear the fit bar, you get fewer, with the reason.

On a website run it adds a three-to-five-minute **sweep** to each visit — pricing, customers, integrations, docs, careers, the footer's "for whom" language — so the profiles rest on what the site says about its own audience, not on the model's priors. When the run is done, `/understudy:run` offers, once, to save the three re-run personas as a target.

### Two things these lenses will not do

- **`aeo` does not query live answer engines.** It judges whether your markup *could* be extracted and attributed — not whether you are cited today. Rate limits, non-determinism and per-query cost put that out of v1, and every `aeo` report says so on its face. A named missing half is a scope decision; an unnamed one is a bug report waiting to happen.
- **`compare` is logged-out only.** It compares public websites. It cannot compare the products behind them — you cannot human-in-the-loop past a competitor's auth wall, and understudy will not create an account on someone else's product to try. It never submits a form on a site you do not own, either: a demo request is a real lead in a real CRM, and a cost imposed on a business that did not ask to be tested.

### Objectives — the part that can fail

Optionally, tell understudy what the product should *do*:

```
Objective        A new user can log a meal from a photo
Success looks    Macros appear within 30 seconds of uploading
```

The persona is told the **objective**. She is never told the **success criterion** — a persona who knows what success looks like will find it, and the test becomes one that cannot fail. A separate scorer sees the criterion for the first time after the evidence is fixed, and returns **achieved · partially achieved · not achieved · not reachable**.

*Not reachable* is deliberately distinct from *not achieved*: a feature behind a paid tier is not a broken feature, and conflating them tells you your product is failing when it is not.

Objectives are never invented. If you give none, the run has none and the report says so.

### Coverage depth — how much gets opened

Asked every run, because it changes the answer:

| | |
|---|---|
| **Overview** | The natural path only. Highest realism — this is what a real first session looks like. Says nothing about screens nobody would find. |
| **Standard** | Natural path plus 2–3 surfaces relevant to the goal. The default. |
| **Deep** | Every reachable surface, after the natural path. Best coverage. |

**Depth and realism genuinely pull against each other**, and understudy says so in the question rather than hiding it. A persona who dutifully opens all nine sections has stopped being a newcomer and become an auditor, and their findings change character with them. So on a `deep` run the traversal marks the moment natural curiosity ran out, and findings after that line are flagged — a finding from a screen no real user would reach is real, but it is not evidence about an ordinary first session.

### Adding a lens

One agent file. That's the whole extension surface.

```yaml
---
name: lens-<slug>
description: <when the orchestrator should invoke this>
mode: A | B | C | D
model: opus | sonnet | haiku
---
```

The body carries the framework, the severity rubric, the output schema and the evidence rule. Drop it in `understudy/agents/` — the orchestrator picks it up, no harness changes.

**Don't use `model: inherit`,** even though the general plugin guidance suggests it. It resolves to the *session* model, which silently re-couples the two model levels — see below.

---

## Watching it run

A product run is an hour or more of a persona thinking aloud into a log file, and Claude Code shows you none of it while it works. So when a run starts it asks one question:

> Open the live view in its own window? Yes / no

Say yes and a terminal window opens on the run. Nothing to type, no path to find — the run command remembers which run it just started. Later, `/understudy:watch` opens the same window for whatever run is newest.

```
 Acme Notes · run 0a1b2c3d · CAPTURE 2 of 3                 ▓▓▓▓▓░░░░░░░░░  07:12 / 45:00
 ───────────────────────────────────────────────────────────────────────────────────────
 WHO IS DOING WHAT                          │ PERSONA · power-user · desktop-1440x900
  ✓ novice           07:00  19 shots        │ [02:32] Clicked the link it gave me. Chrome
  ▶ power-user       07:12  11 shots        │   says this site can't be reached. Great.
  · sceptic          iphone-13              │ [02:40] Fine. Left menu → Classrooms. There
                                            │   it is. Sixteen videos. No date. Where is
 LENSES (after capture)                     │   the live bit?
  · ux           opus    · bugs    sonnet   │ [04:25] Asked for three questions to bring
  · content      opus    · objectives opus  │   to the call. OK — this is the first thing
                                            │   that felt worth the money.
 last shot  09-lesson1-3questions.png       │
 ⏸ PAUSED at the auth wall — log in in the browser, then confirm in Claude Code
```

Left: each persona done, running or pending, with its time against the cap and its screenshot count, then each lens and its model as the fan-out launches and finishes. Right: the persona's own commentary, streamed as it is written — one action behind real time, never a phase behind. The bottom line is the one you need to look up for: the auth pause. Everything on screen is read off the run folder; nothing is inferred and nothing is sent anywhere.

**A one-line version at the bottom of Claude Code.** `/understudy:watch` offers it once — say yes and it is set up; it appears the next time Claude Code starts. It follows the newest run, and clears itself an hour after that run finishes:

`understudy ▶ power-user 07:12/45:00 · 11 shots · Fine. Left menu → Classrooms. There it is.`

(Claude Code does not let a plugin install a status line, so this is the one thing written on your own machine — one entry in `~/.claude/settings.json`, with everything else in the file left as it was and a copy beside it.)

**For the curious**, the script behind both is `understudy/scripts/watch.py` — stdlib only, no install. `watch.py --replay --speed 20` replays a finished run's feed at the persona's own pace, sped up: the quickest way to show someone what the tool does, or to re-live where a persona gave up. It also takes a run folder, or a folder of runs, as an argument.

The lens agents also show under the prompt in Claude Code itself, named for what they are doing (`lens-ux · scoring 3 personas · opus`), and `/tasks` opens any of their transcripts mid-run.

## What a run produces

```
~/.understudy/runs/<slug>/<date>-run-<id>/
├── manifest.json              what ran, on which models, with which personas
├── exec-summary.md            what it is, how it was produced, the Top 5, the personas' own words
├── persona-<name>/
│   ├── screenshots/NN-*.png   one per distinct screen
│   ├── session.log            [MM:SS] one line per action, first person
│   ├── timeline.json          time-to-first-value, steps, permission prompts
│   ├── persona-debrief.md     the four debrief answers, in their own words
│   └── findings-raw.json      reactions — observations, never verdicts
└── <lens>/
    ├── exec-summary.md        that lens's verdict, top 3 and 0–10 score
    └── findings-final.md      severity-rated, every finding evidence-cited
```

**Markdown in the run folder is canonical.** At the end of a run you're offered a rendered copy — exec summary alone, one lens, or everything — in two forms that do different jobs:

- **PDF** — the printed document. Cover with the site's own icon, the summary, every lens report. Goes through headless Chrome; what you forward.
- **Interactive HTML** — one self-contained file for *presenting* the run, no network needed. Dashboard with score rings, Top 5 and persona cards; a findings explorer with severity / check / persona / status filters and a detail drawer; per-persona session replay (the log line by line, with the screen that was showing) and filmstrip; the ICP profiles; a full-screen **Present** mode driven by the arrow keys; a screenshot lightbox; and browser-side **triage** — mark each finding accepted / rejected / fixed with a note, export the result as JSON, CSV or markdown, import a colleague's. Screenshots are embedded downscaled (Pillow, if installed) so a run of 70 screens is ~7 MB; the header takes the site's icon and accent colour.

Both read the same markdown the gate checked; neither scores or rewrites anything. A report whose evidence dies on send is worse than one with no evidence, so both embed their screenshots.

```
understudy/scripts/render_report.py <run_folder> --format html|pdf|print --scope summary|<lens>|all
```

(`print` writes the document layout as HTML without Chromium, for a reader who will Print → Save as PDF themselves.)

**Each lens report stands alone.** They are not deduplicated against each other — a `bugs` report and a `ux` report are different documents for different readers, and each has to make sense on its own. The run-level summary is the one place overlap is reconciled, and it reports it as *corroboration*: **when three lenses that never read each other reach the same finding, that agreement is real signal, not padding.**

**The summary export names each problem once.** Findings that two or more checks raised are grouped into one row under *Raised by more than one check*, with every check's own severity printed beside its name — `Raised by Defects (P0) · Usability (P1) · Content (P1)` — and severities are never averaged. A check's own section then carries only the P0/P1 findings no other check raised, each with what was observed and a screenshot, plus one line saying where the rest went; P2/P3 findings raised by a single check live in the full export. The cover shows both counts — findings and distinct problems — so a 45-finding run reads as the 26 problems it is. Grouping is done on evidence, not wording: the same persona utterance quoted, the same screenshots cited, or a near-identical title. It never groups on product vocabulary, because on an AI product every finding that transcribes a button label would otherwise pair with every other. *(v0.4.1, after a three-lens run showed its worst finding six times.)*

**Every report is written to one house style** — conclusion first, bullets, no prose paragraphs, numbers over adjectives. Not taste: a lens can produce twenty findings and a run can carry seven lenses, and prose does not survive that volume. Concision applies to the *reasoning* only — evidence citations, repro steps and severities are never compressed.

**The evidence is the durable artifact, not the report.** Capture once, score many times — which is why capture over-captures on purpose. The boring screenshot is often the finding.

Findings carry **stable IDs** — `hash(lens + flow + locator + title)`, normalised so that a rewording, a staging host or a changed timing doesn't create a false "new" finding. This is what will let `report --since <run-id>` classify findings as **new · persisting · resolved**. It's built now because it **cannot be retrofitted**: findings written without stable IDs can never be diffed against findings written with them.

---

## Models — you choose, at both levels

An evaluation is a real spend, so understudy asks rather than assumes. Two models run, and understudy controls exactly one.

**Traversal — the session model. understudy cannot change it.** Traversal runs in the main session because the auth pause has to hand you a live browser, and a subagent can't. So it runs on whatever `/model` you're set to. Pre-flight reports which, and if it isn't the strongest available it says so *before* the interview — traversal is the irreversible part, and a weak journey can't be rescued by good scoring afterwards. **It will never claim to have switched models for you.**

**Scoring — yours to pick, per lens.** Lenses are subagents, so these are settable:

| Shape | Allocation | When |
|---|---|---|
| **thorough** | opus everywhere | Best judgement throughout, highest cost |
| **balanced** *(default)* | opus → `ux` `content` `onboarding` `clarity` `conversion` `trust` `icp` `compare`<br>sonnet → `bugs` `seo` `aeo` `technical` | Opus where judgement is load-bearing |
| **cheap** | sonnet everywhere | Fastest; expect weaker `ux` and `content` |

Per-lens overrides accepted. The split exists because `ux` and `content` ask a model to judge whether something is *good* — where a weaker model produces findings that are plausible and wrong, and **a wrong P0 costs more than a missed P2**. `bugs`, `seo` and `aeo` check observable facts against a rubric; the framework carries those.

**Both models land in the manifest.** Findings aren't comparable across models — run Tuesday on one and Friday on another, and a `--since` diff will flag it rather than quietly present the difference as product change.

---

## Personas — read this before trusting a report

Every run asks, explicitly:

- **Generic** — understudy infers personas from the product type alone (novice · power-user · sceptic). Fast, zero input. **The report states on its face that findings rest on inferred personas.**
- **Supplied** — you provide your own. understudy parses them and invents nothing.

**Persona quality, not the harness, is what makes the output good.** Generic personas produce generic findings. The fork is explicit so the limitation is stated rather than silent — but nothing stops you choosing generic every time and trusting the output anyway, and you shouldn't.

One thing worth knowing: when the same behaviour scores P1 for one persona and a non-issue for another, understudy reports it as **two findings and flags the flip** rather than averaging. A flip usually means the product has picked a user without saying so, and averaging destroys the most interesting signal in the run.

---

## This tool never stores your credentials or your product data

The thing clients ask first. By construction, not by discipline.

**Credentials — the agent never handles one.** Not from a file, not from an env var, not from you in chat. At an auth wall it stops and hands you the open browser. The persona never drives an identity provider's UI, and never types a second-factor code. If you offer a password, understudy declines.

**Your data never enters this repo.** Everything real lives in your home directory:

```
~/.understudy/
├── targets/<slug>.yaml     saved only when you say yes; no credentials, ever
├── runs/<slug>/            screenshots, traces, findings — your machine only
├── profiles/<slug>/        browser profiles
└── creds/                  YOURS. understudy reads nothing here, writes nothing here.
```

Nothing is transmitted anywhere. No telemetry, no phone-home, no hosted component. Point the run folder inside the understudy plugin and the interview refuses. Point it inside *your* repo — the default when you run from one — and it is added to that repo's `.gitignore` first, because the run folder holds screenshots of your product.

**The HTML and PDF exports are local files too.** They are written next to the markdown, in your run folder. Nothing uploads them and understudy has nowhere to upload them to — but they embed real screenshots of your product, so once you forward one it is as sensitive as the run itself. That is the point of them; it is worth knowing before you send one.

**And nothing real is in this repo either.** No product names, URLs, credentials, personas or run artifacts — the example target is a fictional product. `.gitignore` has covered targets, runs, `*.env`, `*.png`, `*.webm` and `*.zip` since before the first commit.

---

## How it verifies itself

A tool that produces plausible-looking reports is worse than one that fails loudly, so both halves check themselves and refuse to claim success otherwise.

```bash
scripts/check_capture.py <run>    # after capture
scripts/check_report.py <run>     # after scoring
```

| # | Check | What fails it |
|---|---|---|
| 1 | Evidence rule | A finding with no artifact cited |
| 2 | Naive/analyst separation | Any scoring vocabulary in a capture artifact |
| 3 | Cited artifacts exist | Any finding citing a file that isn't on disk; a P0 citing nothing openable |
| 4 | Stable IDs | A sequence number, a duplicate, or an id that doesn't recompute |
| 5 | Manifest complete | A missing model, persona mode, or exclusions key |
| 6 | Lens report leads with a verdict | A multi-sentence opener, or findings above the top 3 |
| 7 | Score matches severities | A 9/10 above a P0; a score with no reason |

Plus `--expect-lenses N`: the orchestrator says how many lens reports it dispatched, and fewer on disk fails — a lens whose files never landed is otherwise not failed, just not checked.

Check 2 is the one to understand. If it fails, **the fix is to re-run the traversal, not to edit the words out** — the words are a symptom, and deleting them leaves evidence that still confirms its own priors while now passing the check.

Check 6 exists because seven lenses can produce a great deal of unread output. One sentence, then three findings, before anything else.

### And the checks check themselves

`understudy/tests/` holds the plumbing tests — stdlib `unittest`, no model, no browser: one synthetic run per gate check, asserting which check fired; the renderer's fixed reading order, generated index and client-only overall score; a frozen corpus of finding IDs that turns red if normalisation changes. They run on every push via GitHub Actions and build their fixtures in a temp directory, so nothing resembling a real capture is ever committed.

```bash
python3 -m unittest discover -s understudy/tests
```

---

## Run-over-run diffing

```bash
understudy/scripts/compare_runs.py <old_run> <new_run>
```

Matches findings across two runs by **stable ID** — `hash(lens + flow + normalised locator + normalised title)` — and classifies each as **new · persisting · resolved**, with an overlap percentage.

IDs are written from the first run because **they cannot be retrofitted**: findings written without them can never be diffed against findings written with them.

### ⚑ How much understudy disagrees with itself

Measured 2026-09-04. The same evidence was scored twice by the same six lenses on the same models — the capture was held byte-identical, so the only variable is the scoring pass.

| | |
|---|---|
| Findings, run 1 → run 2 | 30 → 30 |
| **Overlap, matched by similarity** | **30.4%** |
| Overlap by exact finding ID | 1.7% |
| P0+P1 overlap | 42.9% |
| Severity moved on a matched finding | 1 (a P0 in run 1 scored P1 in run 2) |

**Read that carefully, because it is the most useful thing on this page.**

**Individual findings are not reproducible. Themes are.** Both runs independently reported: the audience is never stated · four product terms are sold and never defined · the most consequential capability is explained only in the privacy policy · there is no customer proof anywhere · non-existent URLs return 200 · `llms.txt` is absent · canonicals are missing. What changed between runs was how those observations were grouped, worded and scored — not what was seen.

So: **trust the themes, and treat any single finding as one reading rather than a verdict.** If a finding matters enough to act on, the honest move is to open its evidence, which is why every finding cites an artifact you can open.

**A note on the 1.7%.** An earlier version of this README claimed IDs were "normalised so a rewording doesn't create a false new finding." That was wrong, and this measurement is what caught it — hash equality cannot survive a model choosing different words, and one pair here differed by the single word "appears". `compare_runs.py` now matches on similarity as well as ID and prints both numbers, so the diff shows reworded findings as reworded rather than as churn.

**"Resolved" means absent from the new run, which is not the same as fixed.** The lens may not have run; a different model may not have noticed; coverage may not have reached the screen. So the tool prints its comparability warnings **above** the counts, never below, and refuses to present a cross-model or cross-persona-mode diff as though it were clean:

```
⚠ COMPARABILITY — read before the numbers
  · TRAVERSAL MODEL CHANGED: opus → sonnet. Findings are not comparable across
    models; a 'resolved' finding may be a model that failed to notice it.

  new           1
  persisting    8
  resolved      1
  overlap     80.0%
```

Running the same target twice unchanged gives this harness's own noise floor — how much understudy disagrees with itself.

---

## Licence

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Dario Bianchi.
