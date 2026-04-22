# CLI-M4 — Fix All Bugs with Fleet & Guardrails

## ShopSphere CLI Track · Time: 15 min 
Features: `/fleet`, `--autopilot`, `/diff`, `--allow-tool`, `--deny-tool`, `/undo`, `--deny-tool='shell(git push)'`

> **CORE EXERCISE** — Apply all 5 bug fixes using the CLI's parallel `/fleet`
> execution and enterprise guardrails. Review every diff before it is committed.
> Zero accidental pushes.

---

## Objective

Use `copilot` with the `bug-fix-agent` to:

1. Apply all 5 fixes with strict tool permissions — no uncontrolled changes
2. Use `/fleet` to run independent fixes in parallel, reducing total fix time
3. Review every change with `/diff` before accepting
4. Demonstrate `/undo` as the safety net for any bad fix
5. Validate the fixes by running `demo.py` inside the session

---

## Why Fleet + Guardrails?

In production incident response, speed matters — but so does correctness.
`/fleet` lets Copilot run independent tasks concurrently (up to 32 subagents).
`--deny-tool='shell(git push)'` ensures nothing reaches remote until you approve.
Together they give you **parallel speed with manual control on the merge gate**.

---

## Step 1 — Establish a Safe Fix Session

Start a session with the minimum required permissions — no more, no less:

```bash
copilot \
  --agent=bug-fix-agent \
  --allow-tool='read' \
  --allow-tool='edit' \
  --allow-tool='shell(python:*)' \
  --allow-tool='shell(pip:*)' \
  --deny-tool='shell(git push)' \
  --deny-tool='shell(git commit)' \
  --deny-tool='read(.env)'
```

This session can:
- Read any source file
- Edit source files
- Run Python (needed to validate fixes)

This session cannot:
- Push to remote
- Commit to git (you control the commit message and timing)
- Read `.env` (secrets never reach the model)

---

## Step 2 — Run Discovery First

Before fixing, have the agent rediscover the bugs from the code itself
(not from your description). This validates the RCA findings:

```
Scan python-services/checkout-service/app/service/checkout_service.py
and python-services/checkout-service/app/client/payment_client.py for defects.

Present your findings as a numbered list. Do NOT make any changes yet.
Wait for my approval before touching any file.
```

Verify the agent finds the same 5 bugs identified in CLI-M3. If it finds
anything different, investigate before proceeding.

---

## Step 3 — Fix Bugs in Parallel with /fleet

Bugs B1, B2, and B3 are all in `checkout_service.py` but are independent defects.
Bugs B4 and B5 are both in `payment_client.py`. Use `/fleet` to fix both files in parallel:

```
/fleet Fix all 5 bugs found in the discovery scan.

Rules for every fix:
- Minimum viable change only — one or two lines per bug
- Do not refactor, rename, or restructure
- Add a one-line comment explaining why the change was made
- Show a before/after diff for each change

Assign sub-tasks as follows:
- Subagent A: Fix B1, B2, B3 in checkout_service.py
- Subagent B: Fix B4, B5 in payment_client.py

Both subagents work in parallel. Report when complete.
```

`/fleet` spawns two subagents that work concurrently. You will see their
status in the `/tasks` panel. For a production service with many more bugs,
this parallelism is a significant time saving.

Monitor parallel task status:

```bash
/tasks
```

---

## Step 4 — Review Every Change with /diff

When the fleet completes, review all changes before touching git:

```bash
/diff
```

`/diff` shows every uncommitted change in the working directory, with syntax
highlighting. Inspect each fix carefully:

**What to look for in the diff:**

| Bug | Expected change |
|-----|----------------|
| B1 (None discount) | `discount or 0.0` — one-line guard before multiplication |
| B2 (unawaited task) | `result = await payment_coroutine` — `create_task` replaced with `await` |
| B3 (swallowed exception) | `logger.error(..., exc_info=True)` — `exc_info` added |
| B4 (timeout not enforced) | `asyncio.wait_for(...)` wrapping the payment call |
| B5 (no retry) | Retry loop with `asyncio.sleep` between attempts |

If any change looks wrong, revert it immediately:

```bash
/undo
```

`/undo` reverts the last AI-made file change. You can call it multiple times
to step back through changes one by one.

---

## Step 5 — Validate the Fixes

Without committing anything, validate the fixes work:

```
Run python demo.py in python-services/checkout-service and report the result.
Expected: 0% failure rate.
```

Or run directly in the session shell:

```bash
!cd python-services/checkout-service && python demo.py
```

The `!` prefix sends a command directly to your local shell, bypassing Copilot.
Use it to verify without asking the agent to run the command.

Expected output:

```
Results → 10 passed / 0 failed (0% failure rate)
✓ All bugs fixed — checkout is healthy!
```

If the failure rate is still > 0, ask the agent to investigate:

```
The tests still show failures. Read the diff of payment_client.py and
explain why the retry logic might not be activating. Check the exception
type being caught vs the exception type being raised.
```

---

## Step 6 — Controlled Commit (Manual Gate)

The session cannot push — but it can stage and commit if you explicitly
allow it:

```bash
# Review what will be committed
!git diff --staged

# Stage only the service files (not tests or docs)
!git add python-services/checkout-service/app/service/checkout_service.py
!git add python-services/checkout-service/app/client/payment_client.py

# Commit with a structured message
!git commit -m "fix(checkout): resolve P0 incident — 5 production bugs

- B1: guard discount=None before multiplication (checkout_service.py)
- B2: await payment coroutine instead of fire-and-forget (checkout_service.py)
- B3: add exc_info=True to all exception handlers (checkout_service.py)
- B4: enforce config timeout via asyncio.wait_for (payment_client.py)
- B5: add retry loop on transient payment failures (payment_client.py)

Incident: P0-2026-04-21 | RCA: observability/root-cause-analysis.md"
```

> **Note:** The `!` prefix runs these git commands in your shell, not through
> the agent. Git operations are explicitly controlled by you, not the AI.

---

## Step 7 — Run the Full Regression Suite

Before pushing, run the existing tests to confirm no regressions:

```bash
!cd python-services/checkout-service && python -m pytest tests/ -v
```

If tests fail, ask the agent to investigate within the session (it has
context of all the changes it made):

```
These tests are failing: [paste failure output]
Given the fixes applied, which fix is likely incompatible with the existing
test assumptions? Read the test file and the fix, then propose a resolution.
```

---

## Checkpoint ✓

- [ ] Safe fix session started with explicit `--allow-tool` / `--deny-tool` flags
- [ ] Bug discovery confirmed all 5 bugs before any edits
- [ ] `/fleet` used to fix B1–B3 and B4–B5 in parallel
- [ ] `/diff` reviewed — all 5 changes match expected patterns
- [ ] `demo.py` shows 0% failure rate
- [ ] Changes committed with a structured commit message (manually, via `!git`)
- [ ] `pytest tests/` passes

Next: [CLI-M5 Test and PR](./CLI-M5-Tests-and-PR.md)
