---
name: traversal-compare
description: Mode D orchestration. Runs the same capture across two or more sites — the user's and their competitors — keeping each capture independent, then hands the set to the compare lens for a diff pass. Never mixes sites within a capture. Use when the run's objectives include compare.
---

# Traversal — Mode D comparison

**Mode D does not capture anything itself.** It runs Mode A-visit or Mode C once per site, keeps the results apart, and then hands the set over for a diff.

## Load before starting

- Whichever capture skill the comparison is built on — `traversal-visit` (A-visit) or `traversal-crawl` (C)
- `${CLAUDE_PLUGIN_ROOT}/references/evidence-rules.md`

## ⚑ Three constraints that decide whether the output is worth anything

**1. Competitors are user-supplied. Never inferred.**

They come from the target file, named by the user at interview. If none were given, **`compare` does not run** — say so and stop.

> A wrong competitor set produces a confident, useless comparison. The user is the only one who knows whether the site they worry about is the obvious one or the one nobody names, and a plausible guess is indistinguishable from a real answer in the output.

**2. Logged out, always.**

You cannot human-in-the-loop past a competitor's auth wall, and you must not try. **Never create an account on a site the user does not own.** Never submit a form, request a demo, start a trial, or contact anyone. A competitor capture is read-only, and this is not negotiable — it is someone else's business, and a lead in their CRM is a real cost you have imposed on them.

Where a wall appears, record that it exists and stop there. *"Pricing is behind a demo request"* is a finding; getting past it is not your job.

**3. Each site is captured independently, in a fresh context.**

Same persona brief, same shapes, same device, same time cap. **No persona ever sees two sites**, and no capture references another.

> A persona who has just read a competitor is no longer describing this site — they are describing a contrast, and the contrast is Pass 2's job. Capture the sites separately or the comparison compares nothing.

---

## Run order

### 1. Check you can run at all

```
manifest.json → competitors: []   → STOP. Say compare was skipped for want of
                                     user-supplied competitors.
```

Announce the plan and its cost before starting — **N sites means N captures**, and Mode D multiplies everything:

```
→ compare — 3 sites × 1 visit traversal each (25 min cap) ≈ 75 min
```

### 2. Capture each site, in order, the user's site first

```
→ compare [1/3] — <the user's site>
→ compare [2/3] — <competitor A>
→ compare [3/3] — <competitor B>
```

Per site:

1. `browser_close()` first. Fresh context, logged out, no shared state.
2. Run the capture skill unchanged, writing into `compare/<site-slug>/`.
3. Same persona, same device, same cap, same coverage depth. **Any asymmetry invalidates the comparison** — a competitor given five extra minutes will look better, and nothing in the output will reveal why.
4. Record in `compare/<site-slug>/site.json`: the URL, which capture mode ran, when, and **whether anything was unreachable** (a wall, a region block, a robots disallow).

### 3. Score each site independently

Fan out the run's lenses over each site's capture **separately**, exactly as a single-site run would. Site A's `clarity` agent never sees site B.

Output lands in `compare/<site-slug>/<lens>/`.

### 4. Hand over to the diff

Only when every site has been captured and scored: invoke `lens-compare`.

Write `compare/index.json` — the sites, their slugs, which lenses ran on each, and **what could not be reached on which site**. The diff pass needs the asymmetries named, or it will report a gap in coverage as a difference between products.

---

## Things that go wrong

| Situation | Do |
|---|---|
| A competitor sits behind a login | Record it. Capture what is public. **Never create an account.** Note the asymmetry in `index.json`. |
| A competitor blocks automated browsers | Record the block, capture nothing, and say so in the matrix. A site you could not read is not a site that scored badly. |
| One site has far more public pages | Cap all sites at the same depth. Note the difference in `index.json` — it may itself be the finding. |
| The user's site is much slower to capture | Keep the caps equal anyway. Do not give it more time to be fair; that is unfair to the comparison. |
| A competitor's cookie wall blocks everything | Screenshot it, dismiss as a visitor would, continue. If it cannot be dismissed, record that. |
| Only one site captured successfully | **Do not produce a comparison.** Report the single site and say why the others failed. A one-sided matrix reads as a verdict. |

---

## What you do not do

- **Do not infer competitors.**
- **Do not authenticate anywhere**, on any site, in this mode.
- **Do not submit anything** — forms, demos, trials, chat messages.
- **Do not let a persona see two sites.**
- **Do not vary the method between sites** to be generous or thorough.
- **Do not score here.** Capture and hand over.
