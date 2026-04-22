# CLI-M2 — Analyse Logs with Research Agent

## ShopSphere CLI Track · Time: 10 min 
Features: `/research`, `@ file`, `/compact`, `/context`
> **CORE EXERCISE** — Use the CLI's built-in intelligence agents to cross-reference
> production logs against the codebase and produce a precise Bug Inventory —
> the evidence-backed list of what is broken and where.

---

## Objective

Use the CLI's built-in **`explore`** and **`research`** agents, along with the
`log-analysis-agent`, to:

1. Correlate production log errors to specific lines of source code
2. Produce a **Bug Inventory**: file, line, root cause, user impact for each bug
3. Manage context window efficiently across a large log file
4. Demonstrate the `/research` command for deep investigation

---


## Step 1 — Scan the Log File with the Explore Agent

Before going deep, get a rapid orientation of the production logs:

```bash
"Read @observability/production-logs.txt and answer:
1. How many unique error types appear?
2. What are the timestamps of the first and last errors?
3. Which function or method name appears most frequently in the stack traces?
Give me a 10-line summary — nothing more."
```

`explore` is tuned for brevity. It returns focused answers under 300 words,
making it ideal for triage without burning context.

---

## Step 2 — Full Log Analysis with the Custom Agent (Interactive)

Open an interactive session with the `log-analysis-agent` and include both the
log file and the service source in the initial context:

```bash
copilot --agent=log-analysis-agent
```

Inside the session, use the `@` file-inclusion syntax to provide context:

```
@observability/production-logs.txt @python-services/checkout-service/app/service/checkout_service.py

Analyse all errors in the production logs. For each unique error pattern:
1. Quote the exact log line
2. Identify the exact source file and line number where it originates
3. State what runtime condition triggered it
4. Estimate how many users per hour are affected based on log frequency

Format as a numbered Bug Inventory.
```

**The `@` syntax is the CLI's way of injecting file content into context** — equivalent
to `#file:` in VS Code Chat. You can include multiple files in a single message.

---

## Step 3 — Monitor and Manage Context Window

Large log files consume context quickly. Check usage with:

```bash
/context
```

You will see a visualisation like:

```
Context window: 45,231 / 200,000 tokens (22%)
[████████░░░░░░░░░░░░░░░░░░] 22%
```

If you need to add more files without hitting the limit, compact the history:

```bash
/compact
```

`/compact` summarises the conversation history into a single dense summary,
freeing ~70% of the context window while preserving the key findings so far.
This is essential for long incident response sessions.

After compacting, verify the key findings were preserved:

```bash
What are the bugs identified so far? Summarise the Bug Inventory.
```

---

## Step 4 — Deep Research on a Specific Error Pattern

The logs show `TypeError: unsupported operand type(s) for *: 'NoneType' and 'float'`.
Use `/research` to get a thorough analysis of why this happens in the FastAPI/async
context:

```bash
/research How does Python's asyncio event loop interact with None return values
from async functions when those values are used in arithmetic — specifically in
a FastAPI async endpoint that calls an async discount service?
```

`/research` uses the built-in **`research`** agent, which:
- Searches your codebase for relevant patterns
- Fetches relevant GitHub issues and documentation
- Synthesises findings into a structured report

This gives you the "why" behind the error, not just the "what".

---

## Step 5 — Cross-Reference All Five Bug Signals (Non-Interactive)

Use a single non-interactive sweep to produce the complete Bug Inventory:

```bash
copilot --agent=log-analysis-agent
```
```bash
 "You are a senior SRE performing post-incident log analysis. Cross-reference these files:
- observability/production-logs.txt
- observability/incident-report.md
- python-services/checkout-service/app/service/checkout_service.py
- python-services/checkout-service/app/client/payment_client.py
- python-services/checkout-service/config.yaml

Produce a Bug Inventory. For each bug found, include:
- Bug ID (B1, B2, ...)
- File and approximate line number
- Error message or symptom from the logs
- What the code does wrong
- Which users are affected and how frequently
- Severity (P0/P1/P2)

Output as a structured Markdown table."
```

---

## Checkpoint ✓

- [ ] `explore` agent produced a rapid log orientation (Step 1)
- [ ] Bug Inventory produced with file + line + impact for each bug (Step 2)
- [ ] `/context` checked and `/compact` used if needed (Step 3)
- [ ] `/research` ran a deep investigation on the TypeError pattern (Step 4)

Next: [CLI-M3 Root Cause](./CLI-M3-Root-Cause.md)
