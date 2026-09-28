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

1. **What problem does this project solve, and what is its unit of work?** Explain compare model answers using repeatable evidence, identify ai engineers as the audience, and trace one concrete example through the files above. Use the demonstration output rather than hypothetical impact.
2. **Why did you choose the first design decision?** Compare runs on identical case IDs and reject incomplete or mismatched response sets. Show the corresponding implementation and a test that would fail if that property were removed.
3. **How do you protect correctness when inputs or execution change?** Separate actual generated responses, model metadata, latency and token counts from scoring code. Explain the relevant invalid-input or edge-case test and distinguish a checked property from an untested assumption.
4. **How do you make results inspectable and reproducible?** Use paired bootstrap resampling of case-level differences rather than unrelated confidence intervals. Point to actual outputs and recorded commands. Explain why a successful example is weaker evidence than a tested boundary or independently reconciled total.
5. **What would you improve before real deployment or real-data use?** Twelve authored cases; reference token overlap is not factuality, safety or human preference. Local measured latency is hardware-specific. Zero API cost excludes electricity and hardware. Direct/context prompts use the same model, so this is a prompt-configuration comparison. Choose one limitation, describe the missing evidence, and propose a measurable acceptance check rather than promising production readiness.

## Independent exercise

Add a second model adapter and preserve complete case coverage and provenance.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Implemented and validated compare model answers using repeatable evidence using Python · Flask, with dataset validation and documented correctness checks and limitations.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
