# Lab 6: Coverage Analysis Report (photo_print_order)

## 1. Baseline (starter tests)
- Tests: 2 (`test_within_included_prints`, `test_order_valid`)
- Result with `--branch`: 37 statements, 23 missed, 26 branches, 6 partial, **32% coverage**
- Missing lines: 6, 8, 11, 15-23, 28, 30, 35-45. Almost all of `dispatch_status`, the
  error handling, and the pricing logic were untested.

## 2. Code (line) coverage
- Test file: `CodeCoverageTest_photo_print_order.py` (13 tests)
- Command: `python -m coverage run -m pytest CodeCoverageTest_photo_print_order.py`
- Result: 37 statements, 0 missed, **100% line coverage** (screenshot: `code_coverage.png`)
- Strategy: one test per distinct code path so that every line executes at least once:
  both `ValueError` raises, the member bonus, matte vs non-matte rate, the bulk canvas
  surcharge, rush / oversized / normal orders, and the on_time / tight / missed outcomes.
- Limitation: line coverage can hide untested decisions. Running these same tests with
  `--branch` gives 98% and reports a partial branch at `21->23`. The `if finish == "canvas"`
  check is only ever True, because no bulk order uses a non-canvas finish. Every line ran, yet
  one outcome of a decision was never exercised.

## 3. Branch coverage
- Test file: `BranchCoverageTest_photo_print_order.py` (32 tests)
- Command: `python -m coverage run --branch -m pytest BranchCoverageTest_photo_print_order.py`
- Result: 37 statements, 0 missed, 26 branches, 0 partial, **100% branch coverage**
  (screenshot: `branch_coverage.png`)
- Tests added beyond the line-coverage set, to take both True and False outcomes of each decision:
  - `is_member and print_size != "8x10"`: member 8x10 (no bonus), non-member, and member 4x6
  - `extra <= 0`: zero copies and the exact boundary (copies == included)
  - `extra > 50`: boundary at 50 (no surcharge) and 51 (surcharge), with matte, glossy and canvas
  - `finish == "canvas"` inside the bulk block: glossy bulk (the missing `21->23` branch)
  - `order_valid`: rush with 50 and 51 copies, file size 25 and 26, copies 500 and 501
  - `dispatch_status`: framed vs unframed, international vs domestic, and the
    `cutoff - 6` boundary, covering all three return values for each combination

## 4. Conclusion
Line coverage reached 100% with 13 tests, but branch coverage on the same tests was 98%.
Adding 19 more targeted tests, mostly boundary values, brought branch coverage to 100%.
This shows that branch coverage is a stricter measure than line coverage. 