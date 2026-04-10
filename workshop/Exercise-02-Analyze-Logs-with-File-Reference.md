# Exercise 02 — Analyze Logs with `#file`
## ShopSphere Workshop · Time: 5 min · Feature: Copilot Chat + `#file`

> **MANDATORY** — First Copilot skill: attach a file to Chat and extract meaning from logs.

---

### Objective
Use `#file` to point Copilot directly at the production log file and get a structured error analysis — without reading the file yourself.

---

### How `#file` Works
In Copilot Chat, type `#file:` followed by a path (or pick from the dropdown).  
Copilot reads the **full file content** inline and reasons over it.

```
#file:observability/production-logs.txt
```

This is faster than copy-pasting — and works for any file in the workspace.

---

### Step 1 — Open Copilot Chat

Press `Ctrl+Alt+I` (Windows/Linux) or `Cmd+I` (macOS)

---

### Step 2 — Paste This Prompt

```
📋 COPY AND PASTE INTO COPILOT CHAT:

Analyze the log file #file:observability/production-logs.txt

For each distinct error pattern found:
1. Classify the error type (e.g. NullPointerException, swallowed exception, timeout)
2. Identify which user IDs are affected and why
3. Estimate the blast radius — what % of users does this impact?
4. Assign a severity: P0 / P1 / P2

Which issue should I investigate first, and why?
```

---

### What to Look For in Copilot's Response
- Does it identify both error patterns (null crash AND silent payment failure)?
- Does it distinguish user IDs that always fail vs. those that sometimes fail?
- Does it note what's **absent** from the logs (missing stack trace, no correlation ID)?

---

### Checkpoint ✓

Copilot identifies at least **two distinct error patterns** and correctly rates the null crash as higher priority (50% blast radius vs. intermittent payment failures).

**Next:** [Exercise 03 — Map Architecture with Chat](Exercise-03-Map-Architecture-with-Chat.md)
