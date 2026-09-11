# Evals

Everything under here is **fictional**. Nimbus Notes is not a product, the
site is not live anywhere, and every defect in it was planted on purpose.

```
evals/
├── fixture-site/        a marketing site + a tiny app behind a login wall
│   ├── *.html, app/     the pages
│   ├── planted.json     the answer key — what each lens should find, and
│   │                    three things per surface it must NOT report
│   └── serve.py         serves it on localhost for a real-browser capture
└── fixture-run/         two hand-authored captures of that site, frozen
    ├── site/            Mode A-visit (2 personas) + Mode C crawl + Mode B measure
    └── product/         Mode A (2 personas), login wall, run objective
```

## Why the captures are hand-authored

Capture is the expensive, irreversible half; scoring is cheap and needs no
browser. A frozen capture makes every scoring eval byte-reproducible and free
of the browser, so a lens can be scored against identical evidence three
times, or thirty. The screenshots are real renders of the fixture pages; the
logs, timelines, debriefs, crawl records and measurements were written to
describe exactly what those pages contain.

Both captures pass `check_capture.py`. `tests/test_fixture.py` keeps it that
way — a fixture that drifts out of the contract is worse than none.

## What the captures deliberately are not

They are not a measurement of the traversal skills. A traversal eval drives
`fixture-site/` for real (`python3 fixture-site/serve.py`) and is a later,
more expensive layer. These captures test the eleven lenses, the gates and the
renderer against known ground truth.

## Running the lens evals

```bash
python3 understudy/evals/run_evals.py --capture site --lens clarity --lens trust --runs 3
python3 understudy/evals/run_evals.py --capture product --lens bugs
python3 understudy/evals/run_evals.py --trend        # rebuild results/trend.md
```

Each (lens, run) copies the frozen capture to a temp folder, runs the real lens
agent through `claude -p` on the model the manifest allocates, then grades the
two files it wrote. `--dry-run` writes the prompts and calls nothing. Results
land in `results/<timestamp>/`, one line per run is appended to
`results/history.csv`, and `results/trend.md` is rebuilt.

| Grader | How | Kind |
|---|---|---|
| `contract` | `check_report.py --expect-lenses 1` on the output | **Gate.** Pass/fail |
| `recall` | LLM judge: for each planted defect for this lens, did any finding correspond, in any wording | Metric |
| `hallucinations` | LLM judge: was a deliberately clean item reported as a problem | Metric, expect 0 |
| `out_of_lens` | LLM judge: findings that belong to another check | Metric, expect 0 |
| `band` | deterministic: each caught defect's severity vs its planted band | Metric |
| `score` | the 0–10 the lens gave itself | Metric |

**Only `contract` is pass/fail.** The rest are numbers to trend. Do not set a
threshold on any of them until there are enough runs to know the noise — that
is the mistake §11.8 exists to prevent.

## Grading against the answer key

`planted.json` lists each defect with the lenses expected to catch it and the
severity band it should land in. Grade **theme recall** — did any finding
correspond to the planted defect, in any wording — never exact findings, never
counts, never severity equality. The `*_clean` lists are hallucination checks:
a finding that reports one of those as a problem is wrong.
