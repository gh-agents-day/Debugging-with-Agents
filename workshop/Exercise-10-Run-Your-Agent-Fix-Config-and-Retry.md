# Exercise 10 — Run Your Agent to Fix Bugs #4 & #5
## ShopSphere Workshop · Time: 5 min · Feature: Run a custom agent

> **MANDATORY** — Fix Bugs #4 & #5 by invoking the agent you built in Exercise 09.

---

### Objective
Invoke the `oncall-agent` you just built to diagnose and fix the two remaining
bugs — config timeout too low, and no retry logic.

---

### The Remaining Bugs

**Bug #4 — Timeout not enforced** (`payment_client.py` + `config.yaml`)  
`config.yaml` says `timeout: 1` but the payment gateway SLA is 3 seconds.  
Worse: the timeout value is **loaded** from config but **never used** in code.

**Bug #5 — No retry logic** (`payment_client.py`)  
`retry_count: 0` means any transient gateway error = permanent failure.  
The payment gateway has a ~2% real failure rate — but without retry, this
becomes 2% of all orders failing instead of retrying.

---

### Step 1 — Select Your Agent

In Copilot Chat:
1. Click the agent picker (the dropdown or `@` menu)
2. Select **oncall-agent**

---

### Step 2 — Paste This Incident Trigger

```
📋 COPY AND PASTE INTO COPILOT CHAT (oncall-agent selected):

New incident alert — even-numbered users now returning "failed" ~50% of the time.
Server logs show payment errors but no retry attempts.
Config shows timeout: 1 but payment gateway typically takes 2-3 seconds.

Check these files and provide fixes:
#file:python-services/checkout-service/app/client/payment_client.py
#file:python-services/checkout-service/config.yaml
```

---

### Step 3 — Apply Fix #4 (Config Timeout)

In `config.yaml`, change:
```yaml
# Before
timeout: 1

# After
timeout: 5
```

Then apply your agent's suggested code change to `payment_client.py` to **enforce**
the timeout using `asyncio.wait_for()`:
```python
result = await asyncio.wait_for(
    self._call_payment_gateway(user_id, amount),
    timeout=TIMEOUT
)
```

---

### Step 4 — Apply Fix #5 (Retry Logic)

Ask your agent (or Copilot Chat) to generate the retry implementation:

```
📋 COPY AND PASTE INTO COPILOT CHAT:

Add retry logic to PaymentClient.process_payment() in
#file:python-services/checkout-service/app/client/payment_client.py

Requirements:
- Max 3 attempts (loop, not recursion)
- 500ms delay between retries using asyncio.sleep(0.5)
- Log each retry attempt with the attempt number
- Use TIMEOUT from config in asyncio.wait_for()
- On final failure after all retries, return {"status": "error", "reason": "..."}
- Do not change the method signature
```

Review the suggested code and apply it.

---

### Step 5 — Verify

```bash
python demo.py
```

Expected: **all 10 orders pass** (or very close — the random gateway failure
may still affect 1–2 but retries should absorb most).
```
Results → 10 passed / 0 failed (0% failure rate)
✓ All bugs fixed — checkout is healthy!
```

---

### Checkpoint ✓

`python demo.py` shows the "All bugs fixed" message.  
The server logs show retry attempts when the gateway fails transiently.

**Next:** [Exercise 11 — Generate Tests with the CLI](Exercise-11-Generate-Tests-with-CLI.md)
