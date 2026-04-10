# Exercise 04 — Debug a Live Error with `@terminal`
## ShopSphere Workshop · Time: 5 min · Feature: `@terminal` in Copilot Chat

> **MANDATORY** — Core debugging skill: point Copilot at live terminal output to decode real errors fast.

---

### Objective
Trigger the crash live, then use `@terminal` to let Copilot read the error
directly from your terminal — no copy-pasting required.

---

### How `@terminal` Works
`@terminal` tells Copilot Chat to read the **last output** from your active
VS Code terminal. Copilot sees exactly what you see — stack traces, error
messages, log lines — without you having to paste anything.

---

### Step 1 — Start the Server

In a terminal inside VS Code:
```bash
cd python-services/checkout-service
python -m uvicorn main:app --reload --port 8001
```

---

### Step 2 — Trigger the Bug

In a **second terminal**:
```bash
curl -X POST http://localhost:8001/api/v1/checkout \
  -H "Content-Type: application/json" \
  -d '{"user_id": 101, "amount": 150.00}'
```

Switch back to the **uvicorn terminal** — you will see the error output there.

---

### Step 3 — Ask Copilot with `@terminal`

Click on the **uvicorn terminal** to make it the active terminal.  
Then open Copilot Chat and paste:

```
📋 COPY AND PASTE INTO COPILOT CHAT:

@terminal

The checkout API returned {"status": "failed"} for user_id=101.
You can see the server-side error above in the terminal output.

Answer:
1. What is the exact root cause of this error?
2. In which file and on which line does it originate?
3. What is the minimal one-line fix?
4. Is this affecting only user_id=101 or a wider group?
```

---

### What to Observe
- Copilot should identify the file, line, and `TypeError` without you naming them
- If `@terminal` doesn't capture the error, scroll the uvicorn terminal and try again

---

### Checkpoint ✓

Copilot names `checkout_service.py`, the `discount` variable, and the `TypeError`
as the root cause — without you typing any of those words.

**Next:** [Exercise 05 — Find All Bugs with Codebase Search](Exercise-05-Find-All-Bugs-with-Codebase-Search.md)
