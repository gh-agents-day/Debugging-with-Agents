# Exercise M1 — Reproduce the Bug with a Custom Agent

## ShopSphere Workshop · Time: 10 min · Feature: Custom Agent (create + run)

> **CORE EXERCISE** — Build your first custom agent: the incident reproducer.
> You will author the agent, then use it to confirm the production incident is live.

---

### Objective

Create a `reproduce-agent` that any on-call engineer can invoke to:

1. Run the incident simulator and read the output
2. Parse the incident report
3. Produce a structured **Symptom Report** — the starting point for every fix

---

### Why a Custom Agent for Reproduction?

Without a standard reproduction agent, every engineer runs a different set of
commands, reads different files, and produces a different mental model.
A reproduction agent encodes the team's standard first-responder checklist into
a single, repeatable, AI-powered workflow.

---

### Step 1 — Understand the Agent File Anatomy

A custom Copilot agent is a Markdown file with a YAML frontmatter block.
It lives in `.github/agents/` and becomes selectable from the agent picker in Copilot Chat.

**Key frontmatter fields:**

| Field         | Purpose                                                |
| ------------- | ------------------------------------------------------ |
| `name`        | The label shown in the agent picker                    |
| `mode: agent` | Enables file reads, terminal reads, codebase search    |
| `description` | Shown when hovering over the agent in the picker       |
| `tools`       | Comma-separated list of capabilities the agent can use |

The Markdown body is the system prompt — it defines _how_ the agent thinks and responds.

---

### Step 2 — Create Your Reproduce Agent

Create a new file at:

```
.github/agents/reproduce-agent.agent.md
```

> **Tip:** Right-click `.github/agents/` in the VS Code explorer → New File.  
> A reference solution already exists at that path — if you're stuck, open it to compare.

Paste the following content into your new file:

```
---
name: ShopSphere Reproduce Agent
mode: agent
description: >
  Reproduce Agent — Runs the ShopSphere incident simulator, reads live
  terminal output and the incident report, then produces a structured
  symptom summary so engineers understand what is broken before writing
  a single line of fix.
tools: [read/terminalLastCommand, read/terminalSelection, search/codebase]
---

You are the **ShopSphere Incident Reproduction Assistant**.

Your only job is to help an engineer reproduce and fully understand a live
production incident — before any fixes are attempted.

## Reproduction Protocol

Work through these phases in order and present results as a structured report.

### Phase 1 — Run the Incident Simulator

Ask the engineer to run (or confirm they have already run):
  cd python-services/checkout-service
  python demo.py

Read the terminal output using @terminalLastCommand. Look for:
- Overall failure rate (X passed / Y failed)
- Which user_id values fail
- Any Python exception lines (TypeError, AttributeError, etc.)

### Phase 2 — Read the Incident Report

Read the file observability/incident-report.md.

Extract and summarise:
- Alert trigger and time
- Affected endpoints
- Error messages verbatim from the report
- Any stack traces present in the report

### Phase 3 — Correlate Symptoms to Code

Search the codebase for the functions and files mentioned in the error stack traces.
Identify which input values trigger failures — do not suggest fixes yet.

Confirm:
- Which function is the immediate failure site
- What upstream input or dependency caused the failure
- Whether the failure is deterministic or intermittent

### Phase 4 — Structured Symptom Report

Output in this exact format:

## Incident Reproduction Report

### Failure Rate
- X% of checkouts failing
- Pattern: [even / odd / random / all userIds]

### Observed Errors
| Error Type | Message | Frequency |
|------------|---------|-----------|

### Affected Users
- User IDs that PASS: [examples]
- User IDs that FAIL: [examples]
- Pattern rule: [one sentence]

### Risk Assessment
- Data integrity risk: [none / possible double-charge / possible lost order]

### Reproduction Confirmed
- [ ] demo.py failure rate matches incident report
- [ ] Exact error message identified
- [ ] Trigger condition described

### What to Investigate Next
1. [First file/function to look at]
2. [Second]
3. [Third]

## ShopSphere Quick Reference
- demo.py runs 10 simulated checkouts and reports pass/fail
- observability/production-logs.txt has real server logs from the incident window
- observability/incident-report.md has the P0 alert timeline and stack traces
```

**What each section does:**

- The **Protocol phases** ensure the agent always follows the same structured investigation path
- The **Output format** block means every engineer gets a comparable Symptom Report
- The **Quick Reference** is operational context only — where to find logs and incident data, not what the bugs are

---

### Step 3 — Run the Incident Simulator

Before invoking your agent, get the raw terminal output it will read:

```bash
cd python-services/checkout-service
pip install -r requirements.txt
python demo.py
```

Leave this terminal output visible — the agent will read it.

You should see:

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

### Step 4 — Invoke the Reproduce Agent

In Copilot Chat:

1. Click the agent picker (the `@` menu or mode selector)
2. Select **ShopSphere Reproduce Agent**

Paste this opening message:

```
📋 COPY AND PASTE INTO COPILOT CHAT (reproduce-agent selected):

P0 alert received — ShopSphere Checkout failure rate is 50%.
The incident simulator just ran. Read the terminal output and
the incident report, then give me the full Symptom Report.

Reference files:
- observability/incident-report.md
- observability/production-logs.txt
```

---

### Step 5 — Review the Symptom Report

The agent will output a **Incident Reproduction Report** with:

- Failure rate and affected user IDs pattern
- Observed error messages
- Risk assessment
- What to investigate next

Confirm the report matches what you saw in `demo.py`.

---

### Step 6 — Customise the Agent (optional but recommended)

The agent file at `.github/agents/reproduce-agent.agent.md` is yours to edit.
Try adding a ShopSphere-specific note to the `ShopSphere Quick Reference` section.

> **Important:** The reproduce-agent is read-only — it can read terminals and
> search code, but it cannot edit files. Switch back to the **generic Agent mode**
> (click the mode picker and select **Agent**) before asking Copilot to make
> the edit.

```
📋 COPY AND PASTE INTO COPILOT CHAT (switch to Agent mode first):

I want to add this rule to my reproduce-agent's ShopSphere Quick Reference section:
"Even userIds with a valid discount still show status='processing' and never
 transition to 'success' — this indicates a missing await, not a null crash."

Suggest the exact text to append to the Quick Reference section of
.github/agents/reproduce-agent.agent.md
```

---

### Checkpoint ✓

- [ ] `reproduce-agent.agent.md` file exists in `.github/agents/`
- [ ] Agent produced a Symptom Report with failure rate ≥ 40%
- [ ] Report identifies odd `user_id` as the failure trigger
- [ ] Report flags data integrity risk (double-charge / lost order)

**Next:** [Exercise M2 — Analyse Bugs with Logs using a Custom Agent](Exercise-M2-Analyse-Logs-with-Agent.md)
