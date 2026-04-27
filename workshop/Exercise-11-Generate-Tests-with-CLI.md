# Exercise 11 — Generate Tests and Validate with CLI
## ShopSphere Workshop · Time: 5 min · Feature: `copilot` CLI + test-generator agent

> **MANDATORY** — Close the loop: generate regression tests that prove every bug is fixed.

---

### Objective
Generate regression tests for all 5 bug fixes using both the CLI and the
test-generator agent, then run them to confirm all bugs are fixed.

---

### Why Tests Matter Here
Without tests, the 5 bugs could be silently reintroduced in any future commit.  
A regression test is the lasting artifact that makes this incident valuable.

---

### Option A — GitHub Copilot CLI

Use the CLI when you're already in a terminal and don't want to switch to the Chat pane.

> **Prerequisites:** Install the Copilot CLI first (one-time).
> ```bash
> # Windows
> winget install GitHub.Copilot
> # macOS / Linux
> brew install copilot-cli
> # Cross-platform (requires Node.js 22+)
> npm install -g @github/copilot
> ```
> Then authenticate once: run `copilot` in your project directory and enter `/login`.

```bash
# Learn what tests are needed (educational — non-interactive)
copilot -p "Explain pytest tests for a checkout service that was fixed for:
1. discount=None crash for odd userIds
2. asyncio payment not awaited
3. swallowed exceptions without exc_info
Use AsyncMock and @pytest.mark.asyncio"
```

```bash
# Generate a new test file (non-interactive)
copilot -p "Generate a pytest file at tests/test_checkout_service.py
covering the 5 bug fixes in the ShopSphere checkout service"
```

Or start an **interactive session** and ask conversationally:

```bash
cd python-services/checkout-service
copilot
# Then type your question at the prompt, e.g.:
# Generate pytest regression tests for the 5 bugs fixed in checkout_service.py
```

---

### Option B — Test Generator Agent in Chat

Select **test-generator-agent** from the agent picker, then paste:

```

Generate pytest tests for the fixed ShopSphere CheckoutService.

Source file: #file:python-services/checkout-service/app/service/checkout_service.py

The service was fixed to:
1. Treat None discount as 0.0
2. Await the payment coroutine and return its actual result
3. Log exceptions with exc_info=True and include user_id in the message

Generate these 5 tests (use GIVEN/WHEN/THEN in the docstring):
- test_odd_user_gets_zero_discount_no_crash()
- test_even_user_gets_10_discount_applied()
- test_payment_failure_returns_failed_status()
- test_payment_success_returns_success_status()
- test_exception_is_logged_with_user_context()

Use:
- pytest and @pytest.mark.asyncio
- AsyncMock for payment_client and MagicMock for discount_client
- Place the file at: tests/test_checkout_service.py
```

---

### Step — Run the Tests

```bash
cd python-services/checkout-service
python -m pip install pytest pytest-asyncio -q
python -m pytest .\tests\test_checkout_service.py -v
```

Expected output (all green):
```
PASSED tests/test_checkout_service.py::test_odd_user_gets_zero_discount_no_crash
PASSED tests/test_checkout_service.py::test_even_user_gets_10_discount_applied
PASSED tests/test_checkout_service.py::test_payment_failure_returns_failed_status
PASSED tests/test_checkout_service.py::test_payment_success_returns_success_status
PASSED tests/test_checkout_service.py::test_exception_is_logged_with_user_context
5 passed in 0.XXs
```

---

### Final Validation

Run the full incident simulator one last time:

```bash
python demo.py
```

Expected:
```
Results → 10 passed / 0 failed (0% failure rate)
✓ All bugs fixed — checkout is healthy!
```

---

### Checkpoint ✓

- `pytest tests/ -v` → all tests pass (green)
- `python demo.py` → "All bugs fixed — checkout is healthy!"

**You have completed the workshop.**

---

## Bonus Challenges

### Challenge A — Bad Prompt vs. Good Prompt
Send these two prompts to Copilot and compare the quality of responses:
- **Bad:** `fix the bug`
- **Good:** `In checkout_service.py line 28, discount can be None for odd user_ids because get_discount() returns None when no discount tier exists. Fix only this line to default None to 0.0. Do not refactor anything else.`

### Challenge B — Bad Agent vs. Good Agent
Write a deliberately vague agent:
```markdown
---
mode: agent
---
You help debug things. Look at the code and find bugs.
```
Ask it the same incident question as your `oncall-agent`.  
Compare the quality and structure of the response.

### Challenge C — Add Observability
```

The checkout service has no correlation IDs — you can't trace a single
request across the service logs.

Add a FastAPI middleware to checkout_service that:
1. Generates a UUID request_id for each incoming request
2. Adds it to all logger calls in that request context
3. Returns it in the response headers as X-Request-ID

Show me the minimal change to main.py and checkout_service.py only.
```
