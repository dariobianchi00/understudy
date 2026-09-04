# Evidence rules

**[M] methodology.** Binding on capture and on scoring. This is the shortest reference here and the least negotiable.

---

## The rule

> **Every finding cites evidence. No screenshot, log line, or DOM excerpt → the finding is dropped.**

No exceptions. Including — especially — for findings that are obviously true.

**Why "especially":** an obviously-true finding is the one nobody checks. It is also the one most likely to be a model confabulating something plausible about a screen it never opened. The rule exists to make that failure impossible rather than unlikely, and it only works if it is absolute. One exception and it becomes a preference.

---

## What counts

| Evidence | Cited as | Good for |
|---|---|---|
| Screenshot | `persona-<slug>/screenshots/07-consent.png` | Anything visible |
| Log line | `session.log:142` | Sequence, timing, what happened when |
| Console message | `console.log` entry, verbatim | Errors, warnings |
| Network request | Method, URL, status | Failures, latency, unexpected calls |
| DOM excerpt | The actual markup | Structure, markup, accessibility tree |
| Timeline metric | `timeline.json` field | Timings, counts |
| Debrief quote | `persona-debrief.md`, verbatim | What the persona understood |

**What does not count:** *"the persona seemed confused"* without a line where they said so · *"this is standard practice"* · *"users generally expect"* · anything from the target file that was never observed · anything from the model's general knowledge of the product category.

---

## Citation format

Every finding carries at least one:

```markdown
**Evidence:** `persona-novice/screenshots/07-consent.png` · `session.log:142`
> "Why does it need my calendar? It hasn't shown me anything yet."
```

Path relative to the run folder. A quote is verbatim or it is not a quote.

---

## What capture owes scoring

Capture cannot know which observations become findings, so it over-captures on purpose:

- **One screenshot per distinct screen**, even boring ones. The boring screen is often the finding.
- **Console and network at every checkpoint**, and at any moment of confusion.
- **Timestamp everything.** A finding without a time cannot be placed in the journey, and its severity depends on where it happened.
- **Quote the persona verbatim.** Paraphrase destroys the evidence — the exact words are the finding.

A finding dropped for want of evidence is a capture failure, not a scoring failure. Scoring can only work with what it is given.

---

## What scoring owes capture

- **Never invent evidence.** If a finding feels right but has no artifact, drop it. Write it in a "dropped for want of evidence" list if it seems worth chasing — a list nobody will confuse with findings.
- **Never cite an artifact you didn't open.** A screenshot filename is not evidence of what it contains.
- **Never upgrade severity to compensate for weak evidence.** Severity describes impact, not confidence.

---

## The dropped list

Findings dropped for want of evidence go in a clearly-labelled section at the end of the report:

```markdown
## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**
Listed so a future run knows what to look for.

- Signup may be slow on mobile — no timing captured this run.
```

This makes the rule cheap to obey. Without it there is pressure to smuggle a good observation through with weak evidence; with it there is somewhere honest to put it.
