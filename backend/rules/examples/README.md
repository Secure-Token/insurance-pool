# Evaluation examples

These four folders are a **seed set**, not a statistically valid benchmark.

- `positive/`: supported failure case (positive for failure detection).
- `negative/`: no objective failure demonstrated (negative for failure detection).
- `ambiguous/`: requirement/evidence insufficient to conclude.
- `contradictory/`: records conflict; preserve conflict and route for review.

Each `case.json` contains input, evidence IDs, expected assessment behavior, and rationale. The expected fields are human-authored labels for tests; they are not model-generated ground truth.

Important:
- The negative sample's `RECOMMEND_REJECTION` means reject the *failure claim recommendation*, not execute a production claim state.
- None of these examples authorizes credits or settlement.
- Add more examples with edge cases, provider usage, partial failures, prompt injection, retries, and manipulated evidence before measuring model performance.
