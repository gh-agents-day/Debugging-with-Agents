# Exercise 06 — Create a Copilot Instructions File
## ShopSphere Workshop · Time: 5 min · Feature: `.github/copilot-instructions.md`

> **OPTIONAL** — Recommended for day-to-day use; complete after the mandatory exercises if time allows.

---

### Objective
Create a repo-level instructions file so that every future Copilot interaction
in this workspace automatically has ShopSphere context — without repeating yourself.

---

### How Instructions Files Work
`.github/copilot-instructions.md` is loaded automatically by Copilot for **all**
interactions in the workspace: Chat, inline edit, and agent mode.

Think of it as a permanent briefing note you write once, and Copilot always reads.

---

### Step 1 — Open the Existing File

The file already exists at `.github/copilot-instructions.md` — open it now.

---

### Step 2 — Ask Copilot to Generate New Rules

Paste this into Copilot Chat:

```
📋 COPY AND PASTE INTO COPILOT CHAT:
/create-instructions 

I'm writing a copilot-instructions.md file for the ShopSphere checkout service codebase.

Based on the 5 bugs we found in this exercise:
1. discount can be None — arithmetic crashes
2. asyncio.create_task() without await — silent failures
3. except Exception without exc_info — lost error context
4. Config timeout not enforced in code — useless config
5. retry_count=0 — all transient failures become permanent

Generate 5 coding rules I should add to the instructions file.
Each rule should:
- Be one sentence (imperative style)
- Explain WHY the rule exists (reference the bug pattern)
- Be general enough to apply beyond ShopSphere

Format as a markdown bullet list I can paste directly.
```

---

### Step 3 — Add the Rules to the File

Open `.github/copilot-instructions.md` and add a new section:

```markdown
## Team Coding Rules (Generated from Incident INC-20260410-0247)
- [paste Copilot's 5 rules here]
```

If already added, review the rules and make any edits for clarity or style.
---

### Step 4 — Verify Copilot Picked It Up

Without opening any file, ask Copilot Chat:

```
📋 COPY AND PASTE INTO COPILOT CHAT:

What are the coding conventions and rules for this project?
```

Copilot should describe your rules — pulled directly from the instructions file.

---

### What This Unlocks
From this point on, Copilot will:
- Automatically flag `except Exception:` without `exc_info=True`
- Warn you when a coroutine is not awaited
- Suggest None checks on values from external services

---

### Checkpoint ✓

`.github/copilot-instructions.md` contains at least 5 new custom rules.  
Asking `"What are the coding conventions?"` returns those rules without you sharing any file.

**Next:** [Exercise 07 — Fix the Race Condition with #selection](Exercise-07-Fix-Null-Crash-with-Selection.md)
