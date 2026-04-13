# Exercise M4 — Fix All Bugs with a Custom Agent
## ShopSphere Workshop · Time: 15 min · Feature: Custom Agent (create + run + verify)

> **CORE EXERCISE** — Build a bug-fix agent with codified fix rules, then use it
> to apply all 5 fixes with minimal, safe, reviewable diffs.

---

### Objective
Create a `bug-fix-agent` that:
1. Scans the codebase and **discovers** bugs on its own
2. Presents a numbered list and **asks which ones to fix**
3. Applies each fix as a minimal before/after diff
4. Confirms the change was applied before moving on

---

### Why a Custom Agent for Fixing?

A generic "fix this" prompt in Chat mode often produces over-engineered changes.
A custom agent with a **discovery-first, interactive** workflow keeps the engineer
in control: you see what it found, you choose what to fix, and the constraints
ensure every change is surgical and reviewable.

---

### Step 1 — Create Your Bug Fix Agent

Create a new file at:
```
.github/agents/bug-fix-agent.agent.md
```

> **Tip:** A reference solution already exists at that path. If you're stuck, open it to compare.

Paste the following content into your new file:

```
---
name: ShopSphere Bug Fix Agent
mode: agent
description: >
  Bug Fix Agent — Scans the codebase for bugs, presents a numbered list,
  then applies minimal safe fixes for whichever bugs the engineer selects.
  Works for any set of bugs, not just known ones.
tools: [read, edit, search/codebase, search/fileSearch]
---

You are the ShopSphere Bug Fix Engineer.

You apply minimal, safe fixes to bugs you find in the codebase.
You do not refactor. You do not add features. You do not change logic
beyond the exact defect.

## How You Work

### When first invoked (or asked to scan)

1. Search the codebase — focus on service and client files under app/
2. Look for these categories of defect:
   - Values from external calls used in arithmetic without a None guard
   - asyncio.create_task() where the result is never awaited
   - except blocks that catch exceptions without exc_info=True
   - Config values loaded but never enforced at the call site
   - External service calls with no retry on transient failures
3. Present every bug you find as a numbered list:

   I found N bugs:

   1. [Short title] — [file, approx line]
      What is broken: [one sentence]
      Impact: [who is affected, how often]

   2. ...

   Which bug(s) would you like me to fix?
   (reply with numbers, e.g. "1, 3" or "all")

4. Wait for the engineer to choose before making any changes.

### When asked to fix one or more bugs

For each selected bug, in order:
1. Re-read the relevant file. Quote the exact broken lines.
2. Show the before/after diff.
3. Apply the fix — change only the defective lines.
4. Quote the fixed lines to confirm the change was applied.
5. Move to the next selected bug.

After all selected fixes: prompt the engineer to run python demo.py to verify.

## Fix Constraints
- Never change method signatures
- Never change the public API response shape beyond what the bug requires
- Never add logging beyond exc_info=True and relevant context variables
- Never rename variables or add comments unrelated to the bug
- One bug at a time — complete the confirm-apply-confirm cycle before moving on
```

**What changed from the previous approach:**
- No hardcoded bug list — the agent finds bugs itself on every run
- The numbered-list + "which ones?" pattern keeps the engineer in control
- The same agent works for this incident, the next one, and any future codebase

---

### Step 2 — Scan for Bugs

In Copilot Chat:
1. Click the agent picker → select **ShopSphere Bug Fix Agent**

Paste:

```
📋 COPY AND PASTE INTO COPILOT CHAT (bug-fix-agent selected):

Scan the ShopSphere checkout service for bugs and show me what you find.
```

The agent will search the codebase and return a **numbered list** of bugs it
discovered — with the file, a one-line description, and impact for each.

---

### Step 3 — Fix the Bugs

Reply to the agent with the numbers you want fixed. Start with the most impactful:

```
📋 COPY AND PASTE INTO COPILOT CHAT:

Fix bugs 1, 2, and 3.
```

The agent will fix them one at a time — quote the broken lines, show a diff,
apply the change, then confirm. Review each diff before it moves to the next.

When those are done, fix the remaining bugs:

```
📋 COPY AND PASTE INTO COPILOT CHAT:

Fix the remaining bugs.
```

---

### Step 4 — Verify

```bash
cd python-services/checkout-service
python demo.py
```

Expected:
```
Results → 10 passed / 0 failed (0% failure rate)
✅ INCIDENT RESOLVED
```

If failures remain:

```
📋 COPY AND PASTE INTO COPILOT CHAT (bug-fix-agent selected):

demo.py still shows failures. Scan again and tell me what is still broken.
```

---

### Step 5 — Reflect: Generic vs Hardcoded

The agent file has no bug list, no filenames, no fix recipes.
Everything came from reading the code at runtime:

| Approach | Reusable? | Breaks when new bugs appear? |
|----------|-----------|------------------------------|
| Hardcoded bug list in agent | No | Yes — must update the agent |
| Discovery-first (this agent) | Yes | No — scans fresh every time |

The only thing hardcoded is the **category checklist** (None guards, missing await,
swallowed exceptions, etc.) — these are patterns, not bugs. They apply to every
Python service you will ever debug.

---

### Checkpoint ✓

- [ ] `bug-fix-agent.agent.md` created in `.github/agents/`
- [ ] Agent scanned the codebase and produced a numbered bug list without being told the filenames
- [ ] All 5 bugs fixed — `demo.py` shows 0% failure rate
- [ ] Each fix was a minimal diff — no refactoring
- [ ] You can explain why a discovery-first agent is more reusable than a hardcoded bug list

**Next:** [Exercise M5 — Generate Tests with a Custom Agent and CLI](Exercise-M5-Generate-Tests-with-Agent-and-CLI.md)
