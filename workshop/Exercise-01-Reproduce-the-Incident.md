# Exercise 01 — Reproduce the Incident
## ShopSphere Workshop · Time: 5 min · No Copilot needed

> **MANDATORY** — Start here. No Copilot yet; build intuition before you use AI.

---

### Objective
See the bugs in action **before** using any AI tool. Build intuition first — you need to understand the symptom before you can use Copilot effectively.

---

### The Story
Your phone just lit up with a PagerDuty P0 alert at 2:47 AM:
> "ShopSphere Checkout — failure rate 50% and rising. Revenue impact: $12,000/min."

Run the incident simulator and hit the live API to see exactly what's broken.

---

### Step 1 — Setup

```bash
cd python-services/checkout-service
pip install -r requirements.txt
```

---

### Step 2 — Run the Incident Simulator

```bash
python demo.py
```

You should see output like:
```
✓  user=100   $150.00   processing   Regular customer
✗  user=101   $ 89.99   failed       New signup
✓  user=102   $250.00   processing   Premium member
✗  user=103   $ 45.00   failed       Trial user
...
Results → 5 passed / 5 failed (50% failure rate)
⚠  INCIDENT ACTIVE
```

---

### Step 3 — Hit the Live API

```bash
# Start the server in a NEW terminal tab
python -m uvicorn main:app --reload --port 8001
```

```bash
# Even user — passes (or does it?)
curl -X POST http://localhost:8001/api/v1/checkout \
  -H "Content-Type: application/json" \
  -d '{"user_id": 100, "amount": 150.00}'

# Odd user — always fails
curl -X POST http://localhost:8001/api/v1/checkout \
  -H "Content-Type: application/json" \
  -d '{"user_id": 101, "amount": 150.00}'
```

---

### Step 4 — Read the Incident Report

Open `observability/incident-report.md` and read it for 2 minutes.

**Answer these questions (no Copilot yet):**
1. Which user IDs consistently fail? What's the pattern?
2. What two different errors show up in the stack traces?
3. What is critically **missing** from the log output?
4. Is there a risk of double-charges or lost orders?

---

### Checkpoint ✓

You can describe in one sentence why odd user IDs fail.  
Expected demo result: `5 passed / 5 failed (50% failure rate)`

**Next:** [Exercise 02 — Analyze Logs with Chat](Exercise-02-Analyze-Logs-with-File-Reference.md)
