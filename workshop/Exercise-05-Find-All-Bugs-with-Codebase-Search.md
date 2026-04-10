# Exercise 05 — Find All Bugs with `#codebase`
## ShopSphere Workshop · Time: 5 min · Feature: `#codebase` in Copilot Chat

> **MANDATORY** — Search the entire codebase for all 5 bugs at once without reading each file.

---

### Objective
Use `#codebase` to scan the **entire service** for all bug patterns at once —
getting a complete bug inventory before writing a single fix.

---

### How `#codebase` Works
`#codebase` tells Copilot to search across all files in your workspace.  
It's the equivalent of a senior engineer doing a full code review in seconds.

In Copilot Chat, type `#codebase` at the start of your message or attach it
using the paperclip/context menu in the chat input.

---

### Step 1 — Open Copilot Chat

Press `Ctrl+Alt+I`

---

### Step 2 — Full Bug Scan

```
📋 COPY AND PASTE INTO COPILOT CHAT:

#codebase

Search the Python checkout service for these five bug patterns:

1. Any variable received from an external call that could be None,
   used directly in arithmetic without a null/None check

2. Any asyncio.create_task() call where the returned task is
   never awaited and the result is discarded

3. Any except block that catches Exception but does NOT log
   the exception object or call logger.error(..., exc_info=True)

4. Any configuration value that is read from config.yaml at startup
   but never actually enforced in the corresponding code

5. Any retry_count or retry setting that is set to 0,
   meaning failures are never retried

For each finding: give the file path, line number, and one sentence
explaining why it is a bug.
```

---

### Step 3 — Verify the Count

You should get **5 findings** (one per bug pattern).  
If Copilot misses one, try this follow-up:

```
📋 COPY AND PASTE INTO COPILOT CHAT:

You found N bugs. Are there any asyncio.create_task() calls in
#file:python-services/checkout-service/app/service/checkout_service.py
where the task result is never awaited or checked?
```

---

### Expected Findings

| # | Bug | File |
|---|-----|------|
| 1 | `discount` used in `-` without None check | `checkout_service.py` |
| 2 | `create_task()` result never awaited | `checkout_service.py` |
| 3 | `except Exception:` without `exc_info` | `checkout_service.py` |
| 4 | `TIMEOUT` loaded but `wait_for()` never used | `payment_client.py` |
| 5 | `retry_count: 0` — no retry implemented | `config.yaml` / `payment_client.py` |

---

### Checkpoint ✓

Copilot returns at least **4 of 5 bugs** with file + line references.  
You now have a complete bug inventory — ready to fix them one by one.

**Next:** [Exercise 06 — Create a Copilot Instructions File](Exercise-06-Create-Instructions-File.md)
