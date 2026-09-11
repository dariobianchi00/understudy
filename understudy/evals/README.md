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

## Grading against the answer key

`planted.json` lists each defect with the lenses expected to catch it and the
severity band it should land in. Grade **theme recall** — did any finding
correspond to the planted defect, in any wording — never exact findings, never
counts, never severity equality. The `*_clean` lists are hallucination checks:
a finding that reports one of those as a problem is wrong.
