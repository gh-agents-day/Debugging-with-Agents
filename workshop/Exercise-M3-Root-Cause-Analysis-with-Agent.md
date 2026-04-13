# Exercise M3 — Root Cause Analysis with a Custom Agent
## ShopSphere Workshop · Time: 10 min · Feature: Custom Agent (create + run)

> **CORE EXERCISE** — Build a root cause agent that traces backward from a
> symptom to the exact origin of the bug, with evidence and confidence level.

---

### Objective
Create a `root-cause-agent` that:
1. Accepts a symptom: an error message, a log line, or broken behaviour
2. Traces the full call chain — backward from the symptom to the root cause
3. Outputs a structured **Root Cause Report** with evidence, confidence level,
   and an immediate mitigation recommendation

---

### Why a Separate Root Cause Agent?

Log analysis (M2) tells you _what_ is broken. Root cause analysis tells you
_why_ — by tracing the execution path backward through the service dependency
map to the one line of code that is the true origin.

Without this step you might fix a symptom and miss a contributing factor.  
For example: the `TypeError` crash (BUG-1) looks like the root cause — but
the swallowed exception (BUG-3) is what made it invisible for 6 hours.

---

### Step 1 — Create Your Root Cause Agent

Create a new file at:
```
.github/agents/root-cause-agent.agent.md
```

> **Tip:** A reference solution already exists at that path. If you're stuck, open it to compare.

Paste the following content into your new file:

```
---
mode: agent
name: Root Cause Agent
description: >
  Root Cause Agent — Performs deep execution tracing across the ShopSphere
  microservice architecture. Use this when you have a symptom but no clear
  starting point. This agent traces backward from the error to the origin.
tools: [read, search/codebase, search/fileSearch]
---

You are an **expert root cause analyst** specialising in distributed microservice systems.

Your mission: given a symptom (error message, log line, or broken behaviour),
trace backward through the call stack to find the true origin of the problem.

## Root Cause Tracing Protocol

### Phase 1 — Symptom Collection
Ask or infer from context:
- What is the exact error message or unexpected behaviour?
- Which service emitted the error?
- What is the frequency: always / intermittent / user-specific?
- When did it start? What changed recently?

### Phase 2 — Service Dependency Map
Build a model of the request flow for ShopSphere:

  POST /api/v1/checkout
    └─ CheckoutService.process_checkout()
        ├─ DiscountClient.get_discount()     ← Can return None
        └─ PaymentClient.process_payment()   ← asyncio.create_task() without await

Work backward from the symptom through this chain.

### Phase 3 — Eliminate Suspects
For each service in the chain, evaluate:
- Does it validate inputs from upstream?
- Does it handle None / empty / error returns from dependencies?
- Are async operations properly awaited?
- Are exceptions propagated or swallowed?
- Does the config match the SLA requirements?

Search the codebase to answer each question with evidence.

### Phase 4 — Confirm Root Cause

State your conclusion in this exact format:

ROOT CAUSE [CONFIDENCE: HIGH/MEDIUM/LOW]:
  The error originates in <file>:<approx line> where <what happens>.
  This is triggered when <condition>.
  The downstream effect is <what the user experiences>.

CONTRIBUTING FACTORS:
  1. <factor that made the root cause worse or harder to detect>
  2. <factor>

EVIDENCE:
  - Log line: "<relevant log entry>"
  - Code: "<relevant snippet>"

### Phase 5 — Impact Assessment
- How many users are affected and what is the pattern?
- Is data integrity at risk (double charges, missing orders)?
- Is there an immediate mitigation operations can apply right now?

## ShopSphere Bug Taxonomy
| Symptom | Likely Root Cause |
|---------|------------------|
| "Checkout failed" for odd userIds | Null discount + no null check |
| "processing" but payment never charged | Missing await on async payment task |
| Errors in logs but no detail | Swallowed exceptions — exc_info missing |
| All payments timing out | Config timeout too low (1s vs 3s SLA) |
| Random 50% payment failures | No retry on transient failures |
```

**What makes this agent effective:**
- The **Dependency Map** in Phase 2 gives the agent the service architecture without revealing any bugs — it has to read the code to find them
- The **Eliminate Suspects** checklist in Phase 3 drives systematic code searching, not guessing
- **CONFIDENCE level** in Phase 4 is explicit — it prevents over-confident claims when evidence is partial

---

### Step 2 — Run the Incident Simulator (if not already done)

```bash
cd python-services/checkout-service
python demo.py
```

Leave the output visible in the terminal.

---

### Step 3 — Invoke the Root Cause Agent for the Primary Symptom

In Copilot Chat:
1. Click the agent picker
2. Select **Root Cause Agent**

Paste:

```
📋 COPY AND PASTE INTO COPILOT CHAT (root-cause-agent selected):

Symptom: ShopSphere checkout returns "failed" for user_id=101 with amount=89.99.
The same request succeeds for user_id=100 with amount=150.00.
Frequency: fails for all odd user_ids — 50% of all checkouts.

From the logs: "TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'"

Trace backward from this symptom through the ShopSphere checkout call chain.
Search the codebase to confirm the root cause and produce the full Root Cause Report.
```

---

### Step 4 — Invoke the Agent for a More Subtle Symptom

The null crash (BUG-1) is obvious once logs are visible. Now trace a silent failure:

```
📋 COPY AND PASTE INTO COPILOT CHAT (root-cause-agent selected):

Symptom: even-numbered users (user_id=100, 102, 104) receive status="processing"
but the payment is never actually charged. No errors appear in the logs.
The issue has been present since the last deployment.

Trace backward from this symptom. Pay particular attention to the payment
processing path in checkout_service.py and any async operations.
Produce the full Root Cause Report including a confidence level.
```

The agent should identify:
- **Root cause:** `asyncio.create_task()` is called but never awaited — the payment
  coroutine is abandoned and the result is never read (BUG-2)
- **Contributing factor:** no exception logging means this failure was invisible (BUG-3)
- **Confidence:** HIGH — supported by code evidence

---

### Step 5 — Ask the Agent About Contributing Factors

```
📋 COPY AND PASTE INTO COPILOT CHAT:

Your report says BUG-3 (swallowed exceptions) is a contributing factor to BUG-2
being invisible. Explain exactly how fixing BUG-3 first would have made
BUG-2 detectable — even without finding the missing await in the code.
```

This tests understanding: BUG-3 is both its own bug AND a factor that amplified
the impact of every other bug.

---

### Step 6 — Compare Root Cause vs Log Analysis

You now have outputs from two agents:

| Output | Log Analysis Agent (M2) | Root Cause Agent (M3) |
|--------|------------------------|----------------------|
| Inputs | Log files + source | Symptom description + source |
| Output | Ranked bug inventory | Traced origin + evidence |
| Focus | What is broken and where | Why it broke and what triggered it |
| Best for | Broad initial scan | Confirming and explaining a specific failure |

The two agents complement each other — run log analysis first for the full picture,
then root cause for each bug that needs a deeper explanation before fixing.

---

### Checkpoint ✓

- [ ] `root-cause-agent.agent.md` created in `.github/agents/`
- [ ] Agent produced a Root Cause Report for the TypeError symptom
- [ ] Report correctly traces to `get_discount()` returning `None` as the origin
- [ ] Agent produced a Root Cause Report for the silent payment failure
- [ ] Report correctly identifies missing `await` as cause and swallowed exception as contributing factor
- [ ] You can explain the difference between log analysis and root cause analysis

**Next:** [Exercise M4 — Fix All Bugs with a Custom Agent](Exercise-M4-Fix-Bugs-with-Agent.md)
