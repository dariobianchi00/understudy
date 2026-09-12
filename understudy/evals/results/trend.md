# Eval trend

Metrics, never gates (§11.8). One row per lens; the last five runs, newest first. `contract` is the only pass/fail column.

| capture | lens | runs | contract | recall (last 5) | halluc. | out of lens | band ok | score | cost |
|---|---|---|---|---|---|---|---|---|---|
| product | bugs | 4 | 4/4 | 1.0 1.0 0.75 1.0 | 0 0 0 0 | 0 1 0 0 | 1/3 1/4 2/3 2/4 | 2 2 1 1 | $2.73 |
| product | content | 3 | 3/3 | 1.0 1.0 1.0 | 0 0 0 | 0 0 0 | 2/4 0/0 0/0 | 2 2 2 | $6.52 |
| product | onboarding | 3 | 3/3 | 1.0 1.0 1.0 | 0 0 0 | 0 0 0 | 2/2 0/0 0/0 | 2 1 2 | $6.58 |
| product | ux | 3 | 3/3 | 1.0 1.0 1.0 | 0 0 0 | 0 0 0 | 0/0 0/0 2/5 | 2 2 2 | $6.56 |
| site | aeo | 3 | 3/3 | 1.0 1.0 1.0 | 0 0 0 | 0 0 0 | 3/3 2/3 2/3 | 3 5 4 | $2.05 |
| site | clarity | 4 | 4/4 | 1.0 1.0 1.0 1.0 | 0 0 0 0 | 0 0 0 0 | 0/0 0/0 0/0 3/3 | 2 3 2 3 | $7.29 |
| site | conversion | 3 | 3/3 | 0.8 1.0 1.0 | 0 0 0 | 0 0 0 | 4/4 4/5 3/5 | 2 2 2 | $5.16 |
| site | seo | 3 | 3/3 | 1.0 1.0 1.0 | 0 0 0 | 0 0 0 | 4/7 5/7 6/7 | 3 3 4 | $1.85 |
| site | technical | 3 | 3/3 | 1.0 1.0 1.0 | 0 0 0 | 0 0 0 | 0/0 3/3 4/4 | 5 6 6 | $1.73 |
| site | trust | 4 | 4/4 | 1.0 1.0 1.0 1.0 | 0 0 0 0 | 0 0 0 0 | 0/0 3/4 4/4 4/4 | 3 3 3 3 | $7.99 |
