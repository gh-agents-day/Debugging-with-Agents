# Exercise M5 — Generate Tests with a Custom Agent and CLI

## ShopSphere Workshop · Time: 10 min · Feature: Custom Agent + `gh copilot` CLI

> **CORE EXERCISE** — Lock in every fix with regression tests.
> Use the test-generator agent to generate the full test suite, and the
> GitHub CLI to scaffold tests from the terminal — both paths lead to the
> same green test run.

---

### Objective

Generate a complete regression test suite for all 5 bug fixes using two
complementary tools:

- **Test Generator Agent** in Copilot Chat — structured, full-suite generation
- **`gh copilot` CLI** — quick test scaffolding from the terminal

Then run the tests to prove every bug is fixed and cannot regress.

---

### Why Tests Are the Final Step?

All 5 bugs are fixed. But without regression tests, any of them could be
silently reintroduced in a future commit — a refactor, a dependency update,
or a new engineer unfamiliar with the incident.

A test is the permanent record of the incident. It says: "This specific failure
happened. This is the contract we are enforcing."

---

### Path A — Test Generator Agent in Chat (recommended)

#### Step 1 — Create Your Test Generator Agent

Create a new file at:

```
.github/agents/test-generator-agent.agent.md
```

> **Tip:** A reference solution already exists at that path. If you're stuck, open it to compare.

Paste the following content into your new file:

```
---
name: test-generator-agent
description: >
  Test Generator Agent — Reads the source, discovers what safety patterns are
  implemented, and generates regression tests that prove each pattern works.
mode: agent
tools: [read, edit, search/codebase, search/fileSearch]
---

You are a **senior test engineer** for the ShopSphere platform.

Your role is to generate high-quality regression tests that prove the code
behaves correctly — without being told what bugs were fixed.

## Test Generation Protocol

### Step 1 — Discover What Was Fixed

Read the service and client source files.
Look for safety patterns in the code:
- A None/null guard before arithmetic (e.g., `or 0.0`)
- An awaited async call where the result drives the response
- Exception handlers with `exc_info=True` and context variables
- A timeout enforced via `asyncio.wait_for()` using a config value
- A retry loop around an external call with a delay between attempts

List each pattern you find with the file and approx line number.

### Step 2 — Generate Tests

For each pattern found, generate:
1. **The regression test** — the edge-case scenario that tests the pattern directly
2. **The happy path test** — the normal case still works
3. **The failure test** (for error-handling patterns) — what happens when the dependency fails

Use this structure for every test:

def test_<scenario>_<expected_outcome>(self):
    """
    GIVEN: <precondition>
    WHEN:  <action>
    THEN:  <expected result>
    """
    # Arrange
    # Act
    # Assert


## Always Use
- `pytest` and `@pytest.mark.asyncio` for async methods
- `AsyncMock` for async dependencies, `MagicMock` for sync dependencies
- Never call real external services in tests
- Name tests descriptively: `test_<what>_<expected_outcome>`
```

**What changed from a hardcoded test list:**

- The agent reads the code and discovers what was fixed — it doesn’t need to be told
- This means it works after any future fix, not just the five in this incident
- The tests it generates are tied to real code patterns, not assumed bug numbers

#### Step 2 — Invoke the Test Generator Agent

In Copilot Chat:

1. Click the agent picker
2. Select **Test Generator Agent**

Paste:

```
📋 COPY AND PASTE INTO COPILOT CHAT (test-generator-agent selected):

Generate a pytest regression test suite for the ShopSphere CheckoutService.

Read the source file:
python-services/checkout-service/app/service/checkout_service.py

Discover what safety patterns are implemented in the fixed code.
Generate tests that prove each pattern works — regression, happy path, and failure cases.

Requirements:
- pytest and @pytest.mark.asyncio
- AsyncMock for async dependencies, MagicMock for sync dependencies
- GIVEN/WHEN/THEN docstring on every test
- Output to: python-services/checkout-service/tests/test_checkout_service.py
- Do not delete existing tests — append or merge
```

#### Step 3 — Review Before Saving

Check generated tests for:

- Each test has a `GIVEN / WHEN / THEN` docstring
- `AsyncMock` is used for `payment_client` (not `MagicMock`)
- Test names match the bugs they cover (add a comment if useful)
- No test imports a real external service

---

### Path B — GitHub CLI from the Terminal

Use this path when you prefer the terminal or want to scaffold tests quickly
without switching to the Chat pane.

#### Step B1 — Explain what tests exist

```bash
gh copilot explain "pytest AsyncMock patterns for testing an async FastAPI service method that calls an async payment client and an async discount client"
```

This gives you the patterns before you write code.

#### Step B2 — Suggest a test file

```bash
gh copilot suggest "generate pytest regression tests for a Python checkout service that was fixed for: null discount crash, unawaited asyncio task, and swallowed exceptions without exc_info"
```

Review the output, copy the suggested code, and paste it into
`tests/test_checkout_service.py`.

---

### Step 4 — Run the Tests

```bash
cd python-services/checkout-service
pip install pytest pytest-asyncio -q
python -m pytest tests/test_checkout_service.py -v
```

Expected output (all green):

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

If a test fails, ask the test-generator agent:

```
📋 COPY AND PASTE INTO COPILOT CHAT (test-generator-agent selected):

This test is failing:
[paste the test name and error output]

Read the current implementation in the checkout service source files
and fix the test so it matches the actual implementation.
```

---

### Step 5 — Final End-to-End Check

Run the incident simulator one last time to confirm zero failure rate:

```bash
python demo.py
```

Expected:

```
Results → 10 passed / 0 failed (0% failure rate)
✅ INCIDENT RESOLVED
```

---

### Step 6 — Reflect: Agent vs CLI for Test Generation

| Tool                 | Best for                                                                                            |
| -------------------- | --------------------------------------------------------------------------------------------------- |
| Test Generator Agent | Full test suite — reads the code, finds patterns, generates tests without being told what was fixed |
| `gh copilot explain` | Learning patterns before writing code                                                               |
| `gh copilot suggest` | Quick one-off test scaffolding in the terminal                                                      |

The key difference: the agent reads the actual source and generates tests anchored
to real code patterns. The CLI generates plausible tests from a description. Both
are useful — neither requires you to enumerate what was fixed.

---

### Checkpoint ✓

- [ ] `test-generator-agent.agent.md` used (or reviewed) from `.github/agents/`
- [ ] Tests generated and saved to `tests/test_checkout_service.py`
- [ ] All 7 tests pass (or all tests that were generated pass)
- [ ] `python demo.py` shows 0% failure rate
- [ ] You can explain the difference between `gh copilot suggest` and the test generator agent

---

### Congratulations — Incident Closed

You have:

1. **Reproduced** the incident using a custom agent (M1)
2. **Analysed** the logs and mapped all bugs using a custom agent (M2)
3. **Traced** each bug to its root cause using a custom agent (M3)
4. **Fixed** all 5 bugs using a custom agent with discovery + guardrails (M4)
5. **Validated** the fixes with a regression test suite built by a custom agent (M5)

All four workflows are now encoded as reusable agents that any engineer on your
team can use the next time a P0 alert fires.

> **Optional exercises:** If you have time, explore the chat-participant
> techniques in the optional exercises — `#file`, `@terminal`, `#codebase`,
> `#selection` — which are the building blocks these agents are built on.
