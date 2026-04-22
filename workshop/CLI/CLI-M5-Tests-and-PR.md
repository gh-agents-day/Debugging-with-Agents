# CLI-M5 — Tests, Code Review & PR Delegation

## ShopSphere CLI Track · Time: 10 min · Features: `/review`, `--agent=code-review`, `/delegate`, `/pr`, `--output-format=json`, `--share`

> **CORE EXERCISE** — Lock in the 5 fixes with regression tests, run a structured
> code review, and delegate the full PR creation to Copilot — including the PR
> description, linked issue references, and reviewer assignments.

---

## Objective

Use the CLI's built-in **code-review agent**, the `test-generator-agent`, and
`/delegate`/`/pr` to:

1. Generate a full regression test suite for all 5 fixes
2. Run an AI-powered code review against the changes
3. Delegate PR creation to Copilot with a structured description
4. Validate the complete pipeline with `--output-format=json` for CI integration

---

## Why Review + Delegate, Not Just Commit?

In enterprise engineering, bug fixes go through:
1. Code review (correctness + security)
2. Test coverage (regression prevention)
3. PR with context (why, what changed, how to verify)

The CLI can do all three — and the `/delegate` command means Copilot creates
the PR _with_ the correct description, linked issues, and test instructions.
You review and merge. The AI does the paperwork.

---

## Step 1 — Generate Regression Tests

Start a session with the `test-generator-agent`:

```bash
copilot \
  --agent=test-generator-agent \
  --allow-tool='read' \
  --allow-tool='create' \
  --allow-tool='edit'
```

Generate tests that prove each fix works:

```
@python-services/checkout-service/app/service/checkout_service.py
@python-services/checkout-service/app/client/payment_client.py

Generate a pytest regression test suite for all 5 bugs that were fixed.

Read the source files — discover what safety patterns are implemented in the
fixed code, then generate tests that prove each pattern works.

Requirements:
- pytest + @pytest.mark.asyncio for all async tests
- AsyncMock for payment_client, MagicMock for discount_client
- GIVEN / WHEN / THEN docstring on every test
- Test names: test_<what>_<expected_outcome>
- Output file: python-services/checkout-service/tests/test_checkout_service.py

Generate 7 tests minimum:
1. test_odd_user_gets_zero_discount_no_crash
2. test_even_user_gets_10_percent_discount_applied
3. test_payment_success_returns_success_status
4. test_payment_failure_returns_failed_status
5. test_exception_is_logged_with_user_id_and_amount
6. test_payment_timeout_returns_error_status
7. test_payment_retries_on_transient_failure
```

---

## Step 2 — Run the Tests

Validate the generated tests immediately:

```bash
!cd python-services/checkout-service && python -m pytest tests/test_checkout_service.py -v
```

Expected:

```
PASSED tests/test_checkout_service.py::test_odd_user_gets_zero_discount_no_crash
PASSED tests/test_checkout_service.py::test_even_user_gets_10_percent_discount_applied
PASSED tests/test_checkout_service.py::test_payment_success_returns_success_status
PASSED tests/test_checkout_service.py::test_payment_failure_returns_failed_status
PASSED tests/test_checkout_service.py::test_exception_is_logged_with_user_id_and_amount
PASSED tests/test_checkout_service.py::test_payment_timeout_returns_error_status
PASSED tests/test_checkout_service.py::test_payment_retries_on_transient_failure

7 passed in 0.XXs
```

If any test fails:

```
This test is failing:
[paste test name and pytest output]

Read the current implementation and fix the test to match the actual
implementation — do not change the production code.
```

---

## Step 3 — Run the Built-In Code Review Agent

Before creating the PR, run a high-signal code review across all changes:

```bash
/review Review all uncommitted changes in the checkout service for:
1. Security issues (unvalidated input, credential exposure, injection risks)
2. Correctness (does each fix actually resolve the stated root cause?)
3. Async safety (all coroutines awaited, no fire-and-forget patterns remaining)
4. Exception handling (exc_info=True on all except blocks, no swallowed errors)
5. Test coverage (are all edge cases covered by the generated tests?)

Format findings as: SEVERITY | FILE:LINE | FINDING | RECOMMENDATION
```

The built-in `code-review` agent (`/review`) analyses diffs for bugs, security
issues, and logic errors. It has been tuned for high signal-to-noise — expect
fewer but more actionable findings compared to a general prompt.

---

## Step 4 — Address Review Findings

If the review raises any issues, address them in the session:

```
Address all HIGH and MEDIUM severity findings from the code review.
Show a diff for each change made.
```

Re-run the review to confirm findings are resolved:

```bash
/review Confirm that the HIGH and MEDIUM severity findings from the previous
review have been addressed. Output PASS or list any remaining findings.
```
---

## Step 5 — Archive the Full Incident Session

Save the entire CLI-M5 session as the final incident artefact:

```bash
/share gist session
```

This creates a private gist containing:
- All prompts sent
- All code changes made
- Test generation
- Code review findings

The gist URL is the permanent record of how the incident was resolved.

---

## Checkpoint ✓

- [ ] 7 regression tests generated and all pass (Step 1–2)
- [ ] Code review ran — HIGH and MEDIUM findings addressed (Step 3–4)
- [ ] PR created via `/delegate` or `/pr` with structured description (Step 5–6)
- [ ] `demo.py` shows 0% failure rate on the fixed branch (CLI-M4 carryover)
- [ ] Session archived as gist (Step 5)
---

## Congratulations — P0 Incident Resolved via CLI
