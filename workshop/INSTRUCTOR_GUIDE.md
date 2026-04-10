# Instructor Guide — Debug with GitHub Copilot Custom Agents
## ShopSphere Workshop — Facilitator Script

**Duration:** 60 minutes  
**Format:** Instructor-led + Hands-on  
**Room setup:** Participants at their own machines, screen share for demos

---

## Pre-Workshop Checklist

- [ ] All participants have VS Code + GitHub Copilot extension installed and authenticated
- [ ] Repository cloned or available on all machines
- [ ] Python 3.11+ or Java 17 + Maven installed
- [ ] Screen share / projector working
- [ ] Test your demo: `curl` the broken endpoint and confirm it fails
- [ ] Have `observability/production-logs.txt` open and ready to paste

---

## Timing Overview

| Module | Time | Key Activity |
|--------|------|-------------|
| Introduction | 10 min | Concepts + demo |
| Scenario Setup | 5 min | Read incident, reproduce bug |
| Guided Debugging | 25 min | 5-step walkthrough |
| Build Custom Agent | 15 min | Hands-on agent creation |
| Wrap-up | 5 min | Takeaways + reflection |

---

## Module 1 — Introduction to Copilot Agents (10 min)

### Talk Track

> "Before we dive in, let's set the stage. Most of you have used Copilot for code completions and quick questions in chat. Today we're going to use a more powerful mode — Custom Agents."

**Key points to cover:**
1. **Copilot Agents ≠ Copilot Chat** — agents follow a defined protocol, they don't just answer questions
2. Agents are defined as `.prompt.md` files — version-controlled, shareable, team-standardized
3. Today's agents are pre-built — later in the workshop you'll **build your own**

### Live Demo (3 min)

Show the `debug-agent.prompt.md` file open in VS Code:

> "See this file? This is an agent. It tells Copilot how to behave during debugging. It's like giving a junior engineer a detailed runbook — but the 'engineer' is AI, and it never forgets the protocol."

Demo invoking the agent with the incident report:
```
[Open Copilot Chat → select debug-agent]

Here's our incident report from 2 AM:
[paste observability/incident-report.md]

What are the top 3 things I should investigate first?
```

---

## Module 2 — Scenario Setup (5 min)

### Setting the Scene (Read this out loud or display on screen)

> **"It's 2:47 AM. PagerDuty fires. ShopSphere checkout is failing at 60%. Every minute costs us $12,000. The CTO is awake. You have 8 minutes before SLA breach. Here are your tools: logs, the codebase, and Copilot.**
>
> **Let's go."**

### Have participants:
1. Open `observability/incident-report.md` — read for 2 minutes
2. Run the service and reproduce the bug using curl
3. Note their observations (no Copilot yet — build intuition first)

**Ask the room (1 min):**
- "What's your first guess at the root cause, just from reading the incident report?"
- Take 2–3 answers. Don't reveal the answer yet.

---

## Module 3 — Guided Debugging (25 min)

Walk through Steps 1–5 from LAB_GUIDE.md. Do the first two steps as a group demo, then let participants work independently on Steps 3–5.

### Step 1 — Log Analysis (4 min, DEMO)

Share your screen. Open Copilot Chat. Select `debug-agent`.

Paste the log file contents. Show the agent's structured response.

**Teaching point:**
> "Notice the agent gives us a classified finding, not just 'check the code'. That's because we defined a protocol in the agent file. It always leads with impact, then root cause, then confidence level."

**Ask:** "Did the agent spot anything you missed in your first read-through?"

---

### Step 2 — Code Tracing (5 min, DEMO → Hands-on)

Demo opening `checkout_service.py` and asking the root cause agent to trace the flow.

```
[Select: root-cause-agent]

Trace the call from processCheckout() through DiscountClient.getDiscount()
and explain what happens when getDiscount returns None.

[paste checkout_service.py and discount_client.py]
```

**Teaching point:**
> "The agent traces the entire call path for us. In a real incident, this would take an engineer 20–30 minutes of reading. We just did it in seconds."

**Hand off to participants** for Steps 3–5. Give 15–16 minutes.

---

### Circulating the Room (during hands-on time)

Common participant struggles and coaching:

| Struggle | Coaching |
|----------|----------|
| "Copilot isn't finding the bug" | "Add more context — paste both files, not just one. Agents work better with complete context." |
| "I found the bug but don't understand why it's a bug" | "Ask Copilot: 'Explain why asyncio.create_task without await causes a race condition'" |
| "The fix broke something else" | "Ask the test generator agent to check for side effects" |
| "I don't know what to test" | "Use the test-generator-agent — paste your fixed code and ask for regression tests" |

---

### Step 5 Sync (2 min, GROUP)

After hands-on time, sync with the group:

> "Raise your hand if you found all 5 bugs."  
> "Raise your hand if your tests pass after fixing."

**Reveal answers** (write on whiteboard or display):

| Bug | Location | Fix |
|-----|----------|-----|
| Null discount | `checkout_service.py:28` / `CheckoutService.java:42` | `discount = discount or 0.0` / `discount != null ? discount : 0.0` |
| Missing await | `checkout_service.py:37` / `CheckoutService.java:52` | `await payment_task` / `CompletableFuture.get()` |
| Swallowed exception | `checkout_service.py:46` / `CheckoutService.java:59` | `logger.error(..., exc_info=True)` / `logger.error(..., e)` |
| Bad config | `config.yaml:4` / `application.yml:10` | Change timeout from 1 to 5 seconds |
| No retry | `payment_client.py` / `PaymentClient.java` | Add retry loop with 3 attempts |

---

## Module 4 — Build Your Own Agent (15 min)

### Introduction (3 min)

> "Now that you've used pre-built agents, you're going to build your own. This is where the real power is — you can codify YOUR team's debugging knowledge into an agent that any developer can use."

Show the template in LAB_GUIDE.md Module 4.

**Key points:**
- The agent file is just markdown — no coding required
- `mode: agent` makes it appear in the agent picker
- `tools:` controls what the agent can access
- The system prompt defines the agent's behavior and expertise

### Let participants build (10 min)

Circulate and help participants add custom knowledge to their agents.

**Coaching prompts:**
- "What debugging rule do you ALWAYS follow that your teammates forget?"
- "What's the first thing you check when checkout fails in your real codebase?"
- "What common mistakes does your team make that an agent could catch?"

### Share and compare (2 min)

Ask 2–3 participants to share what they put in their agent.

> "See how each agent reflects that engineer's expertise? This is how you bottle team knowledge and make it available to everyone."

---

## Module 5 — Wrap-Up (5 min)

### Key Takeaways (say these explicitly)

1. **Agents = repeatable workflows.** One well-designed agent can onboard your whole team.
2. **Context is everything.** More context (logs + code + config) = better Copilot output.
3. **Swallowed exceptions kill debugging.** Always log with context. Always re-raise.
4. **Async is dangerous.** Every `create_task()` and `@Async` needs a result check.
5. **Fix, then test.** Never close an incident without a regression test.

### Reflection (2 min discussion)

Ask the room:
- "Which bug would have taken you longest to find without Copilot?"
- "What would you change about the debug agent we gave you?"
- "How would you introduce this to your team?"

---

## Frequently Asked Questions

**Q: Can I use these agents in my real project?**  
A: Yes. Copy the `.github/copilot-agents/` folder to your repo and customize the agents with your architecture details.

**Q: How do agents differ from Copilot instructions files?**  
A: Instructions files (`.github/copilot-instructions.md`) apply globally to all Copilot interactions. Agents are opt-in, task-specific workflows you invoke intentionally.

**Q: Do agents remember previous conversations?**  
A: Within a session, yes. Across sessions, no. You can work around this by including relevant context in the agent's system prompt.

**Q: Can agents run code?**  
A: With `tools: terminalLastCommand` and agent mode enabled in VS Code, agents can read terminal output. Full code execution depends on future agent capabilities.

**Q: What's the difference between the 3 agents we built?**  
A: `debug-agent` = Swiss Army knife for any bug. `root-cause-agent` = Deep tracing for hard-to-find bugs. `test-generator-agent` = Validates fixes. Use them in sequence for maximum impact.

---

## Timing Adjustments

**If running behind:**
- Skip Step 4 (timeout config) and Step 5 (retry) from guided debugging
- Give participants the fixed files from `solution/` instead of having them fix independently

**If running ahead:**
- Use the Bonus Challenges from LAB_GUIDE.md
- Run the "Bad prompts vs. Good prompts" comparison as a group exercise
- Have teams compare their custom agents

---

*Facilitator notes last updated: April 2026 | GitHub Copilot Workshop Series*
