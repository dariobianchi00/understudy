---
name: onboarding
description: The understudy interview. Establishes the target product, the objectives, the personas, and the run constraints before any browser opens. Runs on every invocation of /understudy:run — it never assumes and never reuses a target without asking. Use when the user starts an understudy run, asks to evaluate or test a web product, or wants to edit a saved target.
---

# Onboarding — the understudy interview

Runs on every invocation. **Never assumes. One question at a time.**

The output is a **run plan** the user has explicitly approved. Nothing opens a browser until they say go.

---

## Why one question at a time

A nine-part questionnaire in one message gets a three-part answer, and the six missing answers become silent assumptions. Silent assumptions are how an evaluation ends up measuring the wrong product for the wrong person.

Ask, wait, confirm, move on. If the user volunteers several answers at once, accept them, echo them back, and ask only what is still missing.

---

## Step 0 — Look for a saved target

Check `~/.understudy/targets/` for `*.yaml`.

- **Directory missing or empty** → first run. Go to Step 1 without comment. Do not create the directory yet; it is created only if the user chooses to save.
- **Matches found** → list them with their last-run date and ask:

```
Found saved target(s):
  <slug>          last run <date>    <n> objectives
  <slug>          last run <date>    <n> objectives

Reuse one / edit one / start fresh?
```

**Reuse** still echoes the full plan back for confirmation (Step 9). A target saved three months ago may point at a product that has since changed.

**Never** load a saved target and start without confirmation, even if `$ARGUMENTS` named it exactly.

---

## Step 0.5 — Assessment type ⚑ ASKED FIRST, before anything else

**This is the first question of the interview.** It determines every later one: a product interview asks about first value and auth walls, a website interview asks about competitors and conversion goals. Asked in the wrong order you produce an interview that does not fit what the user has.

```
What are you evaluating?

  (a) A product — something people sign into and use.
      Lenses: ux · bugs · onboarding · content
      ~90 min per persona.

  (b) A website — something people read and decide from.
      Lenses: clarity · conversion · trust · technical · seo · aeo · compare
      ~15–25 min per persona, plus a crawl.

  (c) Both — a marketing site with a product behind it.
      Runs (b) on the site, then (a) on the product. Two captures.
```

Record as `assessment_type: product | website | both`. **Never infer it from the URL.** A URL that looks like a marketing site may be the login page of a product, and the two produce entirely different runs.

---

## Step 1 — The target

Ask, in this order:

1. **Product or site name** — used for the slug and report headers.
2. **Base URL** — where a real user or visitor would start. Not a deep link.
3. **Public, or behind auth?** — determines whether Step 6 applies at all.

Derive the slug yourself: lowercase, hyphenated. Show it: `→ slug: acme-notes`.

### If `assessment_type` is website or both — two more, and neither is optional

**⚑ Competitors.** Ask for 1–3 URLs.

> **Never infer them.** A wrong competitor set produces a confident, useless comparison, and the user is the only one who knows whether the site they worry about is the obvious one or the one nobody names.

"None" is a valid answer — say plainly that `compare` will be skipped. Record as `competitors: []`.

**⚑ The conversion goal.** *"What should a visitor do next?"* — sign up, book a call, read the docs, buy, join a list.

> Without it the `conversion` lens has no target and degrades into generic CTA advice. If the user genuinely does not know, record `conversion_goal: null` and tell them `conversion` will report mechanics only.

---

## Step 2 — Lenses (what gets scored)

> Called *objectives* in CLAUDE.md §4. Renamed here because Step 2b introduces **run objectives** — specific claims to prove — and conflating the two is the fastest way to mis-read a plan.

Present the lenses **for the assessment type chosen**, with mode and cost — the cost is the whole point of the architecture.

```
PRODUCT  ·  Mode A — one persona traversal, scored many ways
  ux            Nielsen 10 + HAX 18 + activation
  bugs          console errors, failed requests, dead ends
  onboarding    steps-to-value, time-to-first-value, drop-off
  content       promise-vs-delivery, reading level, jargon

WEBSITE  ·  Mode A-visit — one persona visit, scored many ways
  clarity       can a visitor say what this is, who it's for, what to do next
  conversion    is the next step obvious at every scroll depth
  trust         proof, pricing transparency, who's behind it, data handling

WEBSITE  ·  Mode C — no session, no login
  seo           crawlability, meta, canonical, structured data, sitemap
  aeo           schema.org, answer blocks, entity clarity, llms.txt
                (static markup only in v1 — live answer-engine queries are
                 NOT included; see README)

WEBSITE  ·  Mode B — scripted and measured, no persona
  technical     Core Web Vitals, page weight, image hygiene, headers
                (lab numbers from one machine — never field data)

WEBSITE  ·  Mode D — composes the above across 2+ sites
  compare       same lenses across sites, then a diff pass
```

**Say the cost out loud after they choose.** Adding a lens *within a mode you are already running* is nearly free — it scores evidence already captured. Adding a *mode* means another pass. `clarity + conversion + trust` is **one** visit; `clarity + seo` is **two** captures in different modes. Users routinely assume more lenses means proportionally more time; the surprise runs the other way.

---

## Step 2a — Coverage depth ⚑ asked every run

How much of the product or site should the persona actually open? **This changes the answer, so the user chooses it — it is not a default buried in a reference file.**

```
How deep should I go?

  (a) Overview   — the natural path only. Highest realism: this is what a
                   real first session looks like. Says nothing about screens
                   nobody would find.

  (b) Standard   — natural path + 2–3 surfaces relevant to the goal.  [default]

  (c) Deep       — every reachable surface, after the natural path.
                   Best coverage. But past a point the persona has stopped
                   being a newcomer and become an auditor, and I will mark
                   which findings came from that stretch.
```

**State the trade-off in the question, not afterwards.** Depth and persona realism genuinely pull against each other, and a user who picks `deep` should know they are buying coverage with realism.

**Check it against the time cap (Step 5) before the plan is echoed.** `deep` on a 30-minute cap is not deliverable — say so now, not after the run. Record as `coverage_depth`.

---

## Step 2b — Run objectives ⚑ optional, and never invented

Ask once:

> **Is there anything specific you want this run to test?** Something the product should let someone do, that you want proved or disproved.

If no → record `objectives: []` and move on. Most runs have none.

If yes, per objective capture **two** things, in the user's own words:

- **The objective** — *"A new user can log a meal from a photo."*
- **The expected outcome** — what success looks like, observably. *"Macros appear within 30 seconds of uploading."*

```
Objective        A new user can log a meal from a photo
Success looks    Macros appear within 30 seconds of uploading
```

**Three rules, all load-bearing:**

- **⚑ The persona is told the objective. The persona is NEVER told the success criterion.** She is asked to try logging a meal from a photo; she is not told what "working" looks like. A persona who knows the criterion will find it, and the result is a test that always passes. This is the naive/analyst separation (§6, invariant 1) applied to objectives, and it is the easiest thing in the design to break.
- **Captured now, before capture.** An objective the persona never pursued cannot be scored honestly afterwards.
- **Never invent one.** If the user declines, the run has none and the report says so. An inferred objective scored as "achieved" is the worst output this tool could produce.

---

## Step 3 — Personas ⚑ an explicit fork, asked every run

Never skip this. Never infer it from context. Ask it plainly:

```
Personas — two options:

(a) Generic. I propose personas from the product type and your objectives
    alone. Defaults: novice · power-user · sceptic. Fast, zero input from you.
    ⚠ The report will state on its face that findings rest on INFERRED
      personas. This materially weakens the findings.

(b) Supplied. You paste your own persona definitions, or point me at a file.
    I parse them and invent nothing.

Which?
```

**Why this is a visible fork and not a default:** persona quality — not the harness — is what makes the output good, and persona quality cannot ship in a public repo. Making the choice explicit turns a silent limitation into a stated one.

- **(a) Generic** → propose 3 personas, one paragraph each: who they are, what they want from this product, what they'd give up on. Get approval on the set before continuing. Record `persona_mode: generic` in the target file — it propagates to the report's face.
- **(b) Supplied** → read what they give you. **Parse, do not embellish.** If a supplied persona lacks a goal or a device, ask; do not fill it in. Record `persona_mode: supplied`.

Then ask **how many personas** for this run. More personas multiply wall time linearly — the traversal is the expensive part, and each persona is its own traversal.

---

## Step 4 — Device profile per persona

Ask per persona, not once for all. A persona who is mobile-dominant and one who is desktop-only are testing different products.

Common profiles: `desktop-1440x900` · `desktop-1920x1080` · `iphone-13 (390x844)` · `android (393x844)`.

If a persona is defined by their device — a desktop-only user, a phone-only user — **record that as a constraint, not a preference.** It must not be silently overridden later.

---

## Step 4a — Models ⚑ confirm both levels, assume neither

Two models run in a single evaluation, and understudy controls exactly one of them. Be straight about which.

### Traversal model — you cannot change it, so report and recommend

Pre-flight already surfaced the session model. Restate it here in cost terms, because this is where the user is deciding what to spend:

```
Traversal will run on: <session model>

I can't change this — only you can, with /model. It's the irreversible
part: the persona decides what to do next, and a weak journey can't be
rescued by good scoring afterwards.

<n> personas × 90 min all run on this model.
```

If they want a different one: `/model <name>`, then re-invoke `/understudy:run`. The saved target survives, so nothing is lost.

**Never** claim to have switched models. **Never** pin a lens to a model as a workaround for a session-model concern — they are different levels and conflating them produces a run whose manifest lies.

### Scoring models — this one is yours to choose

Scoring runs as subagents, so the model is per lens. Show the default and the two alternatives, with the trade-off named:

```
Scoring models — three shapes:

  (a) thorough    opus on every lens
                  Best judgement everywhere. Highest cost.

  (b) balanced    opus  → ux, content, onboarding, compare
      ← default   sonnet → bugs, seo, aeo
                  Opus where judgement is load-bearing; sonnet where the
                  framework does the work and the task is closer to
                  extraction against a checklist.

  (c) cheap       sonnet on every lens
                  Fastest and cheapest. Expect weaker ux and content
                  findings — those lenses are judgement, not extraction.

  Or override per lens. Which?
```

**Why balanced splits where it does:** `ux` and `content` ask a model to judge whether something is *good*, and a weaker model produces findings that are plausible and wrong — the most expensive failure mode, because a wrong P0 costs more than a missed P2. `bugs`, `seo` and `aeo` check observable facts against a rubric: was there a console error, is there a canonical tag, is there valid schema.org. The framework carries those.

**Resolve the shape to concrete model names now, and write those names into the target file.** Do not store the shape alone and resolve it later — resolve against what is available at this moment, so the recorded choice is the choice that runs. Lens files declare a default; the orchestrator passes the confirmed name explicitly at call time and never relies on inheritance.

**Record both models in the run manifest.** Findings are not comparable across models. A user who ran Tuesday on one model and Friday on another has two runs that cannot honestly be diffed, and the manifest is what lets a future `--since` comparison flag that instead of silently presenting it.

---

## Step 5 — Time cap per traversal

Default: **90 minutes** per persona, with a hard stop.

**Compute the total and show it before they agree:**

```
3 personas × 90 min = 4.5 hours of traversal
                    + ~1 hour of scoring
                    ≈ 5.5 hours total
```

This is the single most common surprise in a run. If their window is shorter, offer: fewer personas · a shorter cap · or splitting across two sittings (the run folder supports persona-by-persona progression).

---

## Step 6 — Auth

Skip entirely if Step 1 said public site.

Otherwise ask: **is there a wall, and where?** — a login page, an SSO redirect, an identity proxy in front of the whole domain, a paywall mid-flow.

Then confirm the human-in-the-loop pause, verbatim:

```
When the traversal hits the wall, it stops and hands you the open browser:

  → [persona] traversal — auth wall detected at <url>
  ⏸  PAUSED — authenticate in the open browser, then confirm
  → [persona] traversal — resuming at <path>

I never see, store, or type a credential. The persona never drives an
identity provider's UI — it stops at the wall and hands over.

The auth wall is also never reported as a finding. It's infrastructure,
not a product defect.
```

**Never** offer to read a credentials file, accept a password in chat, or "just this once" handle a token. If the user offers one, decline and restate the pause.

---

## Step 7 — Output destination

Default: `~/.understudy/runs/<slug>/`.

Accept an alternative if they want one, with one check: **if the path is inside this repo, refuse and explain.** Real run artifacts — screenshots, traces, findings about a real product — must never land in a public repo. Offer the default instead.

---

## Step 8 — Scope exclusions

Ask: **is there anything that must NOT be reported as a finding?**

Give the canonical example so the question lands:

> e.g. an identity proxy in front of the product is infrastructure, not a UX
> defect — it's a deployment stage, and reporting it wastes a P0 slot.

Other common ones: a known-broken staging feature · a deliberately unfinished section · anything already on the roadmap.

Record them verbatim. Exclusions are applied at **scoring** time, not capture — the traversal still records what it sees, the analyst drops it. That distinction matters: an excluded thing that blocks the persona still explains why they got stuck.

---

## Step 9 — Echo the plan back, then wait

Print the plan in full. **Wait for an explicit go.** Do not proceed on silence or on an ambiguous reply.

```
RUN PLAN — <product name>
─────────────────────────────────────────────────────
Assessment    <product | website | both>
Target        <slug>  ·  <base-url>
Auth          <none | wall at <where>, human-in-the-loop pause>
Competitors   <urls, or "none — compare skipped">      (website only)
Goal          "<conversion goal>"                       (website only)

Lenses        Mode A-visit → clarity, conversion, trust
              Mode C       → seo

Coverage      standard — natural path + 2–3 surfaces
Objectives    1 — "A new user can log a meal from a photo"
              (persona is told the goal, never the success criterion)

Personas      3, INFERRED (generic)        ← flagged in the report
              novice        desktop-1440x900
              sceptic       iphone-13

Captures      3 × Mode A-visit traversal  (25 min cap each)
              1 × Mode C crawl            (no session)

Scoring       3 lenses over the visit evidence, in parallel
              1 lens  over the crawl evidence

Models        traversal   <session model>   (session-set; I can't change it)
              scoring     balanced — opus: clarity, conversion, trust
                                     sonnet: seo

Excluded      <verbatim list, or "nothing">
Output        ~/.understudy/runs/<slug>/

Estimated     ~1.5h traversal + ~30m scoring
─────────────────────────────────────────────────────
Go?
```

The **captures vs. scoring** split is the line that teaches the architecture. Keep it.

---

## Step 10 — Offer to save the target

Only after the plan is approved:

```
Save this target for next time?
  → ~/.understudy/targets/<slug>.yaml
  Outside the repo, gitignored. Credentials are never saved.
```

On yes, write the file. Create `~/.understudy/targets/` if needed. Schema in `${CLAUDE_PLUGIN_ROOT}/examples/target.example.yaml`.

**Never written to the target file:** passwords, tokens, cookies, session state, or anything from `~/.understudy/creds/`. That directory is user-created and user-owned; understudy reads nothing from it and writes nothing to it.

---

## Failure modes to avoid

| Anti-pattern | Why it's wrong |
|---|---|
| Asking all nine questions in one block | Gets partial answers; the rest become silent assumptions |
| Defaulting personas to generic without asking | The fork is the honesty mechanism (Step 3) |
| Reusing a saved target without confirming | The product may have changed since |
| Starting a traversal without an explicit go | The user is committing hours; make them say yes |
| Accepting a credential "to speed things up" | Non-negotiable — see Step 6 |
| Writing run output inside the repo | Public repo; see Step 7 |
| Quoting a time estimate only after they commit | Step 5 exists to prevent exactly this |
| Inferring the assessment type from the URL | A marketing URL may be a product's login page. Step 0.5 |
| Inferring competitors | A wrong set produces a confident, useless comparison. Only the user knows |
| Running `conversion` with no goal | It degrades into generic CTA advice indistinguishable from a real finding |
| Defaulting coverage depth silently | It changes the answer; the trade-off against realism is the user's to make |
| Telling the persona the success criterion | Guarantees the objective passes. The single easiest way to break invariant 1 |
| Inventing an objective the user did not ask for | An inferred objective scored "achieved" is the worst output this tool can produce |
| Assuming a scoring allocation without asking | It's the user's spend; Step 4a exists to make the trade-off theirs |
| Claiming to have switched the session model | The harness cannot. Saying otherwise makes the manifest a lie |
| Pinning a lens model to compensate for a weak session model | Different levels. Scoring cannot rescue a weak traversal |
