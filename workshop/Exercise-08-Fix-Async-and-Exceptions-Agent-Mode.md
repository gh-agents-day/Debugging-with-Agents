# Exercise 08 — Fix Bug #2 & #3 with Agent Mode
## ShopSphere Workshop · Time: 5 min · Feature: Copilot Agent Mode (multi-file edit)

> **MANDATORY** — Fix Bugs #2 & #3 using Agent mode across multiple files simultaneously.

---

### Objective
Use **Agent mode** to fix two bugs across two files at once:
- Bug #2: `asyncio.create_task()` not awaited (race condition)
- Bug #3: exceptions swallowed without context (useless error logs)

---

### How Agent Mode Works
Agent mode moves beyond answering questions — it **edits files** directly.  
It reads your codebase, proposes changes, shows a diff, and asks for confirmation.

Switch to Agent mode: Copilot Chat → click the mode selector → **Agent**

---

### The Bugs

**Bug #2** — `checkout_service.py` (around line 37)
```python
# BROKEN: task is started but result is never checked
payment_task = asyncio.create_task(
    self.payment_client.process_payment(user_id, final_amount)
)
return {"status": "processing", ...}  # returns before payment finishes!
```

**Bug #3** — `checkout_service.py` (around line 46) and `payment_client.py`
```python
# BROKEN: exception is caught but context is lost
except Exception:
    logger.error("Checkout failed")   # no user_id, no amount, no stack trace
    return {"status": "failed"}
```

---

### Step 1 — Switch to Agent Mode

In Copilot Chat, click the mode selector → select **Agent**

---

### Step 2 — Paste This Task

```
📋 COPY AND PASTE INTO COPILOT CHAT:

Fix two bugs in the ShopSphere checkout service:

BUG 2 — Missing await in checkout_service.py:
The asyncio.create_task() call starts payment processing but the result
is never awaited. The method returns "processing" immediately.
Fix: replace create_task() with a direct await so the caller waits for
payment to complete. If payment fails, return status="failed". If it
succeeds, return status="success".

BUG 3 — Swallowed exceptions in checkout_service.py and payment_client.py:
The except blocks catch Exception but do not log the exception details.
Fix ALL except blocks in both files:
- Change `except Exception:` to `except Exception as e:`
- Change bare logger.error("...") to logger.error("...", exc_info=True)
- Include user_id and amount in every error log message

Do not change any business logic beyond these two fixes.
After editing, show a summary of every line changed.
```

---

### Step 3 — Review the Diff

Agent mode will:
1. Show you a **diff** of proposed changes
2. Ask for confirmation before saving
3. Apply changes to both files

Review the diff carefully — check that:
- `await` replaces `create_task()` in checkout_service.py
- `exc_info=True` is added to every `logger.error()` call
- No other logic has changed

---

### Step 4 — Verify

```bash
# Restart the server to reload changes
# Then run the simulator
python demo.py
```

Expected: even user IDs now sometimes return `"failed"` (instead of always `"processing"`) — exposing Bug #5 (no retry). The uvicorn logs now show full exception details.

---
(If you already fixed Bug #1, you'll see payment errors with full context instead.)

**Next:** [Exercise 09 — Build Your Own Debug Agent](Exercise-09-Build-Your-Debug-Agent.md)
