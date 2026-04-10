# Lab Guide — Debug with GitHub Copilot Custom Agents
## ShopSphere Production Incident Workshop

**Duration:** 60 minutes  
**Your Role:** On-call engineer responding to a P0 production incident

---

## The Incident

> **02:47 AM — PagerDuty fires.**
>
> "P0 ALERT: ShopSphere Checkout — failure rate 60% and rising. Revenue impact $12,000/min. SLA breach in 8 minutes."
>
> You open your laptop. Slack is going wild. The VP of Engineering is already in the war room. You have the logs, the codebase, and GitHub Copilot.
>
> **Your job: Find the bugs. Fix them. Get checkout back online.**

---

## Setup (Before You Begin)

### Prerequisites
- VS Code with GitHub Copilot extension installed
- Python 3.11+ **or** Java 17 + Maven

### Clone and Run (Pick your language)

**Python:**
```bash
cd python-services/checkout-service
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8001
```

**Java:**
```bash
cd java-services/checkout-service
mvn spring-boot:run
```

### Reproduce the Bug
```bash
# Trigger a failing checkout (odd userId)
curl -X POST http://localhost:8001/api/v1/checkout \
  -H "Content-Type: application/json" \
  -d '{"user_id": 101, "amount": 150.00}'

# Trigger a "successful" checkout that silently loses payment (even userId)
curl -X POST http://localhost:8001/api/v1/checkout \
  -H "Content-Type: application/json" \
  -d '{"user_id": 100, "amount": 150.00}'
```

**Expected (broken) output:**
```json
{"status": "failed"}
{"status": "processing"}   ← payment may never have run!
```

Open [`observability/production-logs.txt`](../observability/production-logs.txt) and [`observability/incident-report.md`](../observability/incident-report.md) — these are your starting artifacts.

---

## Module 1 — Understand Copilot Agents (10 min)

### What are Custom Agents?
Custom Agents in GitHub Copilot are **reusable, task-specialized AI assistants** defined as `.prompt.md` files. Unlike inline suggestions, agents follow a structured protocol to handle complex, multi-step tasks.

**Copilot Modes:**
| Mode | Best For |
|------|----------|
| Inline completions | Line-by-line code writing |
| Copilot Chat | Questions, explanations, quick fixes |
| Custom Agents | Workflows: debugging, test generation, code review |

### Your Agents (Pre-built for this workshop)

Open these files in `.github/copilot-agents/`:

| Agent | File | Purpose |
|-------|------|---------|
| Debug Agent | `debug-agent.prompt.md` | Analyze logs + code → root cause + fix |
| Root Cause Agent | `root-cause-agent.prompt.md` | Trace execution path from symptom to origin |
| Test Generator Agent | `test-generator-agent.prompt.md` | Generate tests to validate your fix |

**How to invoke an agent:**
1. Open GitHub Copilot Chat (`Ctrl+Alt+I`)
2. Click the agent picker icon or type `/` to select an agent
3. Choose your agent from the list
4. Paste your context (logs, code, error message)

---

## Module 2 — Read the Incident (5 min)

Open [`observability/incident-report.md`](../observability/incident-report.md).

**Answer these questions before touching any code:**

1. What two different errors are showing in the stack traces?
2. Which user IDs consistently fail?
3. When did the incident start? What changed?
4. What is the risk of data loss (double charges)?

> **Pro tip:** Use Copilot Chat to summarize the incident:
> ```
> Summarize this incident report and list the top 3 questions I need 
> to answer to resolve the incident.
> ```
> Paste the contents of `incident-report.md` into the chat.

---

## Module 3 — Guided Debugging with Copilot (25 min)

Work through these 5 steps in order. Each step has a Copilot prompt to use.

---

### Step 1 — Analyze the Error Log

**Open:** `observability/production-logs.txt`

**Use Copilot Chat (or Debug Agent):**
```
Analyze this production log from our checkout service. 
Identify: 
1. Error patterns 
2. Which user IDs are affected 
3. Possible root causes
4. Urgency/priority of each issue

[paste log contents here]
```

**What to look for:**
- Which user IDs always fail vs. sometimes succeed
- The time gap between "Processing complete" and "Payment processing failed"
- What the logs DON'T tell you (missing context is itself a clue)

**Checkpoint:** Can you explain in one sentence *why* odd user IDs fail?

---

### Step 2 — Trace the Code Flow

**Open:**  
- Python: `python-services/checkout-service/app/service/checkout_service.py`  
- Java: `java-services/checkout-service/src/main/java/com/shopsphere/checkout/service/CheckoutService.java`

**Use Copilot Chat:**
```
Trace the execution flow of the processCheckout method.
For each step, identify:
1. What data passes between functions
2. What could be null or fail
3. Where exceptions could be swallowed
```

**Use Root Cause Agent** for deeper analysis:
```
[Select: root-cause-agent]

I have a checkout service returning {"status": "failed"} for user_id=101 
but working for user_id=100. 

Trace this behavior through the code and find why even/odd user IDs behave differently.

[paste checkout_service.py and discount_client.py]
```

**Checkpoint:** Can you point to the exact line number of Bug #1?

---

### Step 3 — Find the Root Cause

Now dig into the async bug — the sneakiest one.

**Open:**  
- Python: `app/client/payment_client.py` AND `app/service/checkout_service.py`
- Java: `client/PaymentClient.java` AND `service/CheckoutService.java`

**Use Debug Agent:**
```
[Select: debug-agent]

Our checkout service returns {"status": "processing"} but payments 
never complete. Users are NOT being charged, but orders are created.

This is a P0 incident causing revenue loss.

Analyze this code and explain the async/threading issue:

[paste checkout_service.py]
[paste payment_client.py]
```

**Questions to answer:**
1. What does `asyncio.create_task()` / `@Async` do differently from `await`?
2. When the payment task raises an exception, who sees it?
3. Why does the checkout always return "processing" even when payment fails?

**Checkpoint:** You should now be able to name all 5 bugs in the system.

---

### Step 4 — Fix the Bugs

Work on the fixes one at a time. **Use Copilot to suggest the fix**, then review it before applying.

#### Fix #1 — Null Discount (Bug #1)

**In `checkout_service.py` / `CheckoutService.java`:**
```
The variable 'discount' can be None/null. 
Fix: if discount is None, treat it as 0 (no discount).
Make the fix minimal — don't change anything else.
```

#### Fix #2 — Race Condition / Missing Await (Bug #2)

**Prompt:**
```
Fix the asyncio.create_task() / @Async issue so that:
1. The checkout waits for payment to complete
2. If payment fails, checkout returns {"status": "failed"}
3. If payment succeeds, checkout returns {"status": "success"}
```

#### Fix #3 — Swallowed Exceptions (Bug #3)

**Prompt:**
```
The catch/except block logs "Checkout failed" but loses the exception details.
Fix it to log the full exception with stack trace and context (user_id, amount).
```

#### Fix #4 — Config Timeout (Bug #4)

**Open:** `config.yaml` / `application.yml`

**Prompt:**
```
The payment timeout is 1 second but the gateway SLA is 3 seconds.
Also, the timeout value is never actually enforced in the code.
Fix config.yaml and payment_client.py to enforce the timeout.
```

#### Fix #5 — No Retry (Bug #5)

**Prompt:**
```
The payment client has no retry logic.
Add retry with:
- Max 3 attempts
- 500ms delay between retries
- Log each retry attempt
```

---

### Step 5 — Validate with Tests

**Use Test Generator Agent:**
```
[Select: test-generator-agent]

I've fixed the following bugs in CheckoutService:
1. discount can be None — now defaults to 0
2. payment was not awaited — now properly awaited
3. exceptions were swallowed — now logged with context

Generate test cases in Python/Java for each fix that:
- Prove the bug is fixed (regression tests)
- Cover the happy path
- Cover the edge cases

[paste your fixed checkout_service.py]
```

**Run the tests:**
```bash
# Python
pytest python-services/checkout-service/tests/ -v

# Java
cd java-services/checkout-service && mvn test
```

**Checkpoint:** All tests should pass. If any fail, go back to Step 4.

---

## Module 4 — Build Your Own Debug Agent (15 min)

Now you'll create a custom agent tailored to YOUR debugging style.

### Task: Create a "ShopSphere On-Call Agent"

This agent should be the first thing you invoke during any future incident.

**Create a new file:** `.github/copilot-agents/oncall-agent.prompt.md`

Use this template:
```markdown
---
mode: agent
description: First-responder agent for ShopSphere production incidents
tools:
  - codebase
  - githubRepo
---

You are the ShopSphere on-call debugging assistant.

When given an incident alert, your first response is always:

1. **Triage**: Is this a crash, data issue, or performance issue?
2. **Blast radius**: What % of users are affected? Which services?
3. **Immediate action**: Is there a quick mitigation (config rollback, feature flag)?
4. **Investigation plan**: 3 steps to diagnose the root cause

Then, ask: "Do you want me to start Step 1 now?"

[Add your own debugging rules and ShopSphere-specific knowledge here]
```

### Customize your agent:
- Add the bug patterns you discovered in this workshop
- Add ShopSphere architecture notes
- Add your own debugging checklist items

### Test your agent:
```
[Select: YOUR new oncall-agent]

New incident: Payment service is returning 500 errors for all requests.
Started 5 minutes ago. No recent deployments.

Here are the last 20 log lines:
[paste a section of production-logs.txt]
```

Does your agent give a useful, structured response?

---

## Module 5 — Wrap-Up (5 min)

### What You've Learned
- Custom Agents = **repeatable debugging workflows** you define once and reuse forever
- Copilot finds bugs **faster** when you give it structured context (logs + code together)
- **Swallowed exceptions** are the hardest bugs to find — always log with context
- **Async bugs** require special attention — always check if tasks are awaited
- A well-designed agent is like having a **senior engineer on call 24/7**

### Reflection Questions
1. Which bug would have taken you longest to find manually?
2. What would you add to your personal debug agent?
3. How would you share this agent with your whole team?

---

## Bonus Challenges

If you finish early, try these:

### Challenge A — Memory Leak Hunt
```
Simulate a memory leak by adding a global list that grows on each request.
Use Copilot to detect and fix it.
```

### Challenge B — Performance Issue
```
Add a deliberate N+1 query pattern in the discount lookup.
Use Copilot to identify the pattern and suggest a fix.
```

### Challenge C — Bad Prompts vs. Good Prompts
Compare these two prompts and evaluate the quality of Copilot's responses:

**Bad prompt:** `fix the bug`

**Good prompt:**
```
In checkout_service.py line 28, discount can be None for odd user IDs 
because discount_client.get_discount() returns None when no discount exists.
Fix only line 28 to handle None by treating it as 0.0. Do not refactor 
anything else.
```

---

## Reference

| File | Purpose |
|------|---------|
| `observability/incident-report.md` | The incident you're solving |
| `observability/production-logs.txt` | Live production logs |
| `.github/copilot-agents/debug-agent.prompt.md` | Debug agent |
| `.github/copilot-agents/root-cause-agent.prompt.md` | Root cause agent |
| `.github/copilot-agents/test-generator-agent.prompt.md` | Test generator |
| `workshop/PROMPT_CHEATSHEET.md` | Ready-to-use prompts |
| `workshop/DEBUG_CHECKLIST.md` | Debugging checklist |

---

*Good luck, engineer. The war room is watching. 🚀*
