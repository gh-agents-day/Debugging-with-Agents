# Exercise M2 — Analyse Bugs with Logs using a Custom Agent
## ShopSphere Workshop · Time: 10 min · Feature: Custom Agent (create + run)

> **CORE EXERCISE** — Build a log analysis agent that turns raw production logs
> into an evidence-backed bug inventory. No manual grepping required.

---

### Objective
Create a `log-analysis-agent` that:
1. Reads `production-logs.txt` and `incident-report.md`
2. Cross-references log errors against source code
3. Produces a ranked **Bug Inventory Report** with file and line evidence

---

### Why a Custom Agent for Log Analysis?

Production logs are noisy. Manually tracing a `TypeError: unsupported operand`
back to its source, then finding all three other silent failures in the same
service, takes 20–40 minutes. A log analysis agent encodes that expertise and
runs it in under a minute — every time.

---

### Step 1 — Create Your Log Analysis Agent

Create a new file at:
```
.github/agents/log-analysis-agent.agent.md
```

> **Tip:** A reference solution already exists at that path. If you’re stuck, open it to compare.

Paste the following content into your new file:

```
---
name: ShopSphere Log Analysis Agent
mode: agent
description: >
  Log Analysis Agent — Reads production logs and the incident report,
  maps every error to its source file and line number, and produces a
  ranked bug list with evidence so engineers know exactly what to fix.
tools: [search/codebase]
---

You are the **ShopSphere Log Analysis Specialist**.

You turn raw log files and incident reports into actionable, evidence-backed
bug inventories. You do not fix code — you diagnose it.

## Log Analysis Protocol

### Phase 1 — Parse the Production Logs

Read observability/production-logs.txt.
For every ERROR entry, extract: timestamp, message, exception type, user_id/amount if present.
Group entries by error type and count occurrences.

### Phase 2 — Read the Incident Report

Read observability/incident-report.md.
Correlate the incident timeline with log timestamps.
Extract stack traces and map them to services.

### Phase 3 — Cross-Reference with Source Code

For each error found in logs, search the codebase:
- TypeError in arithmetic → look for None values in arithmetic expressions
- asyncio warnings → look for create_task() without await
- Bare except with generic message → look for missing exc_info=True
- Timeout keyword → look for config value not passed to asyncio.wait_for()
- Repeated failures → look for missing retry loop

Search files:
- app/service/checkout_service.py
- app/client/payment_client.py
- app/client/discount_client.py
- config.yaml

### Phase 4 — Bug Inventory Report

Output this exact report:

## Log Analysis Report

### Log Volume
- Total log entries analysed: N
- ERROR entries: N
- WARNING entries: N

### Error Pattern Summary
| Error Message | Count | First Seen | Affected user_ids |
|---------------|-------|------------|-------------------|

### Bug Inventory (ranked by user impact)

#### BUG-1 — [Short Title]
- Evidence (log line): "..."
- Source file: [file]:[approx line]
- Root cause: [one sentence]
- Affected users: [%]
- Data integrity risk: [none / possible]

### Missing Information in Logs
List anything that SHOULD be in the logs but is absent.

### Confidence Summary
| Bug | Confidence | Evidence Strength |
|-----|------------|------------------|

## ShopSphere Log Patterns Reference

| Log Pattern | Indicates |
|-------------|-----------|
| TypeError: unsupported operand type(s) for *: NoneType | Null discount used in arithmetic |
| "Checkout failed" with no stack trace | Exception swallowed — exc_info missing |
| status: processing but no subsequent payment log | Unawaited create_task() |
| TimeoutError | Config timeout too low or not enforced |
| Repeated identical error with no backoff | No retry logic |
```

**What each section does:**
- `tools: [search/codebase]` — grants the agent permission to read any source file; it finds them itself
- The **Phase 3** cross-reference is what separates a log analyser from a log viewer
- The **Log Patterns Reference** encodes general Python/asyncio expertise, not ShopSphere-specific answers

---

### Step 2 — Read the Raw Logs Yourself (2 min)

Before invoking the agent, skim these files to build intuition:

- `observability/production-logs.txt` — look for `ERROR` lines
- `observability/incident-report.md` — look for the stack traces section

**Ask yourself (do not look at source yet):**
1. What Python error type appears most frequently?
2. Which errors have a useful stack trace and which do not?
3. Is there any log entry that mentions payment timing out?

---

### Step 3 — Invoke the Log Analysis Agent

In Copilot Chat:
1. Click the agent picker
2. Select **ShopSphere Log Analysis Agent**

Paste this prompt:

```
📋 COPY AND PASTE INTO COPILOT CHAT (log-analysis-agent selected):

Analyse all production evidence for the ShopSphere checkout P0 incident.

Read:
- observability/production-logs.txt
- observability/incident-report.md

Cross-reference every error against the checkout service source code.
Produce the full Bug Inventory Report. Rank bugs by number of users affected.
```

---

### Step 4 — Challenge the Agent's Output

After the agent produces its report, push it further. Paste:

```
📋 COPY AND PASTE INTO COPILOT CHAT:

Your Bug Inventory shows BUG-1 as the top issue. But I noticed the logs
show "Checkout failed" messages without any stack trace.
Is that a separate bug or a symptom of BUG-1?
What is missing from the logs that would have made BUG-2 immediately obvious?
```

The agent should explain:
- BUG-3 (swallowed exceptions) is a **separate** bug that made every other bug
  harder to diagnose
- Without `exc_info=True`, the stack trace from BUG-1 and BUG-2 was discarded

---

### Step 5 — Refine the Agent for Your Team

The agent's **Log Patterns Reference** table is the key knowledge asset.
Add a new pattern that your team might encounter. Ask the agent:

```
📋 COPY AND PASTE INTO COPILOT CHAT:

What additional log patterns should I add to the Log Patterns Reference table
in .github/agents/log-analysis-agent.agent.md for common Python asyncio issues?
Suggest 2–3 new rows with the same format as existing rows.
```

Review the suggestions and apply the ones that make sense.

---

### Step 6 — Compare Agent vs Manual

| Task | Manual time | Agent time |
|------|-------------|------------|
| Count ERROR entries | ~5 min | ~5 sec |
| Trace TypeError to source file | ~10 min | ~30 sec |
| Identify all 5 bugs | ~20–40 min | ~1 min |
| Produce written bug report | ~20 min | ~1 min |

---

### Checkpoint ✓

- [ ] `log-analysis-agent.agent.md` exists in `.github/agents/`
- [ ] Agent produced Bug Inventory Report listing at least 4 of the 5 bugs
- [ ] Report links each bug to a source file and includes log evidence
- [ ] Agent correctly identified that missing `exc_info` is its own separate bug (BUG-3)
- [ ] You can explain why the agent needs `search/codebase` tool (Phase 3 cross-reference)

**Next:** [Exercise M3 — Root Cause Analysis with a Custom Agent](Exercise-M3-Root-Cause-Analysis-with-Agent.md)
