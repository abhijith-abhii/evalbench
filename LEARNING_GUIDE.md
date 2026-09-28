# EvalBench — learning guide

## What it does

Compare model answers using repeatable evidence. The intended user is ai engineers. Browser controls → validated Flask API → project analysis/workflow → results and export.

## Run and demonstrate

Follow the README installation block, then: Run run_models.py to generate both actual model runs. Compare their paired scores, inspect individual failures and change the left/right selection. Identical runs produce zero difference.

## Important files

- `app.py` — local HTTP interface and request/error handling.
- `core.py` — project-specific logic.
- `tests/` — regression and correctness checks.
- `reports/` — recorded outputs and verification evidence.

## Three engineering decisions

1. Compare runs on identical case IDs and reject incomplete or mismatched response sets.
2. Separate actual generated responses, model metadata, latency and token counts from scoring code.
3. Use paired bootstrap resampling of case-level differences rather than unrelated confidence intervals.

## Five interview questions

1. **What is compared?** Actual local FLAN-T5-small answers under direct and context-assisted prompts on twelve authored QA cases. The toolkit compares these measured runs rather than claiming a general model ranking.

2. **Why require matching case IDs?** If systems answer different cases, aggregate scores are not comparable. Coverage checks ensure the paired comparison uses the intended same evaluation set.

3. **Why report exact match and token F1?** Exact match rewards identical normalized answers; token F1 gives partial overlap credit. Both can miss semantic correctness, so individual outputs remain available for review.

4. **Why use a paired bootstrap?** Sampling case pairs preserves the correspondence between systems on each example. The interval reflects uncertainty from this small case set, not every possible user query.

5. **How are bad model answers handled?** They are retained in the committed run artifacts and included in scores. The project does not replace errors with ideal fixture answers or discard unfavorable cases.

## Independent exercise

Add a second model adapter and preserve complete case coverage and provenance.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Evaluated actual local FLAN outputs under two prompt strategies using exact match, token F1, coverage validation and paired bootstrap intervals across twelve authored cases.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
