# Exercise 09 — Build Your Own Debug Agent
## ShopSphere Workshop · Time: 5 min · Feature: Custom `.prompt.md` Agent

> **MANDATORY** — Create your own reusable debug agent. This is the core skill of the workshop.

---

### Objective
Create a reusable on-call debug agent that any engineer on your team can invoke
during a production incident — encoding everything you learned in this workshop.

---

### How Custom Agents Work
A `.prompt.md` file in `.github/agents/` becomes a **selectable agent**
in Copilot Chat. It defines:
- What role Copilot plays
- What structure it always follows
- What domain knowledge it has about your system

You write it once. Every engineer gets a consistent, expert first-responder.

---

### Step 1 — Create the Agent File

Create a new file at:
```
.github/agents/oncall-agent.agent.md
```

---

### Step 2 — Paste This Starter Template

```
📋 COPY AND PASTE INTO oncall-agent.agent.md:

---
name: ShopSphere On-Call Agent
mode: agent
description: ShopSphere On-Call Agent - First-responder for production incidents
tools: [search/codebase, web/githubRepo]
---

You are the ShopSphere on-call debugging assistant.
You are the first AI the team talks to during a production incident.

When given an alert, error message, or log snippet, ALWAYS respond
with this exact structure:

## Triage
- Error type: [null crash / async issue / swallowed exception / timeout / retry failure]
- Affected scope: [all users / odd userIds / even userIds / random %]
- Data integrity risk: [none / possible double-charge / possible lost order]
- Quick mitigation available: [yes - describe it / no]

## Root Cause Hypothesis
State the most likely root cause in one sentence.
Point to the file and line number if known.

## Investigation Steps
1. [Most likely place to look first]
2. [Second thing to check]
3. [Third thing to check]

## Known ShopSphere Patterns
- Null discount: get_discount() returns None for odd userIds — callers must null-check
- Missing await: asyncio.create_task() without await means payment result is never seen
- Swallowed exceptions: except without exc_info=True hides the stack trace
- Timeout not enforced: config.yaml timeout must be used in asyncio.wait_for()
- No retry: retry_count=0 means every transient failure is permanent

Ask: "Shall I start with Step 1?"
```

---

### Step 3 — Ask Copilot to Review and Improve It

```
📋 COPY AND PASTE INTO COPILOT CHAT:

Review my new agent at #file:.github/agents/oncall-agent.agent.md

Based on the 5 bugs from the ShopSphere incident (INC-20260410-0247),
suggest 2-3 additional patterns to add to the "Known ShopSphere Patterns"
section so a future engineer using this agent would catch similar bugs faster.
```

Add the suggestions to the file.

---

### Checkpoint ✓

The file `.github/agents/oncall-agent.agent.md` exists with:
- A `mode: agent` frontmatter
- A structured triage format
- At least 5 ShopSphere-specific known patterns

**Next:** [Exercise 10 — Run Your Agent to Fix Bugs #4 and #5](Exercise-10-Run-Your-Agent-Fix-Config-and-Retry.md)
