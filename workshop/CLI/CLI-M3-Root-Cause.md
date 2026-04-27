# CLI-M3 — Root Cause Analysis in Plan Mode

## ShopSphere CLI Track · Time: 10 min 
Features: `--plan`, `/plan`, `--mode=plan`, `/session plan`, `Shift+Tab`

> **CORE EXERCISE** — Use the CLI's Plan Mode to construct a structured,
> evidence-backed Root Cause Analysis before any code is changed. Plan mode
> forces deliberate thinking: analyse first, act second.

---

## Objective

Use `--plan` mode with the `root-cause-agent` to:

1. Build a structured Root Cause Analysis (RCA) document before touching code
2. Trace each bug backwards from symptom → log evidence → code defect → line
3. Validate the plan (the RCA) before approving execution
4. Demonstrate the `Shift+Tab` mode cycle: interactive → plan → autopilot

---

## Why Plan Mode for Root Cause Analysis?

Root cause analysis is about structured thinking, not speed. Plan mode in
the Copilot CLI **separates the "what to do" from the "doing it"**: the agent
builds an actionable plan first, presents it for your review, and only executes
after you approve.

In incident response, this is the difference between:
- An engineer who jumps to fixing code and introduces new bugs
- An engineer who maps the fault tree first, then makes surgical changes

---

## Step 1 — Start the Root Cause Agent in Plan Mode

```bash
cd path/to/Debugging-with-Agents

copilot --agent=root-cause-agent --plan
```

`--plan` starts the session in plan mode. 

Inside the session, you will see the plan-mode indicator. Submit the RCA prompt:

```
@observability/production-logs.txt
@observability/incident-report.md
@python-services/checkout-service/app/service/checkout_service.py
@python-services/checkout-service/app/client/payment_client.py
@python-services/checkout-service/config.yaml

Perform a Root Cause Analysis on the ShopSphere P0 incident.

For each bug in the Bug Inventory, trace the causal chain:
1. Observable symptom (what users experienced)
2. Log evidence (exact log line with timestamp)
3. Code path (which function was executing)
4. Defect (what the code does wrong at a specific line)
5. Root cause (why this code path leads to this failure)
6. Fix hypothesis (one-sentence description of the minimal change needed)

Present this as a structured RCA document. Do NOT make any file changes yet.
```

The agent will respond with a complete plan. Review it.

---

## Step 2 — Review and Validate the Plan

Examine the generated RCA plan. Ask clarifying questions before approving:

```
For Bug B2 (unawaited asyncio task): explain why the payment result is lost
and not just delayed. Show the exact execution path using the code.
```

```
For Bug B4 (config timeout not enforced): what would the actual runtime
behaviour be if timeout=1 is set in config.yaml but asyncio.wait_for()
is never called?
```

Plan mode lets you interrogate the analysis before committing. This is the
review checkpoint every senior engineer would do.

---

## Step 3 — Check Session Plan Status

Inside the session, view the structured plan:

```bash
/session plan
```

This shows the plan the agent built, formatted as a structured checklist.
Use it to confirm all 5 bugs are captured before proceeding.

---

## Step 4 — Switch Modes with Shift+Tab

The CLI supports three modes: **interactive → plan → autopilot**.

Press `Shift+Tab` to cycle through modes without restarting the session.

Try it:
1. Press `Shift+Tab` once — switches from plan to autopilot
2. Ask: "Summarise the RCA findings in 5 bullet points"
3. Observe the response — autopilot executes without pausing
4. Press `Shift+Tab` again — back to interactive mode

This mode cycling means you can switch between deliberate analysis (plan) and
fast execution (autopilot) within a single session.

---

## Step 5 — Run RCA Non-Interactively with `--mode=plan`

For team environments where the RCA must be reproducible and reviewable, use
`--mode=plan` with `-p` to generate the analysis document programmatically:

```bash
copilot \
  --agent=root-cause-agent \
  --mode=plan \
  --effort=high \
  --allow-tool='read' \
  --deny-tool='edit' \
  --deny-tool='create' \
  -p "Read the source files and incident report, then produce a complete Root Cause
Analysis document for the ShopSphere P0 incident. Include causal chain, code
evidence, and fix hypothesis for each of the 5 bugs. Output as Markdown."
```

The `--deny-tool='edit'` and `--deny-tool='create'` flags ensure no file
changes are made — this is a read-only analysis pass.

---

## Step 6 — Export the RCA as a Shareable Artefact

```bash
/share file ./observability/root-cause-analysis.md
```

Or create a private GitHub gist:

```bash
/share gist session
```

The shared RCA document becomes the official incident record. It is referenced
in the post-incident review and informs future runbook updates.

---

## Step 7 — Approve and Exit Plan Mode

Once the RCA is validated:

```
The RCA looks correct. Please summarise it as 5 fix directives — one sentence
each — that the Bug Fix Agent can use as input in the next exercise.
```

Copy the 5 fix directives. You will use them as the input prompt in CLI-M4.

Type `/exit` to close the session.

---


## Checkpoint ✓

- [ ] Root cause agent started in `--plan` mode
- [ ] RCA produced — 5 bugs with causal chains and fix hypotheses
- [ ] Plan reviewed using `/session plan`
- [ ] `Shift+Tab` mode cycling demonstrated
- [ ] RCA exported as Markdown file in `observability/`


Next: [CLI-M4 Bug Fix](./CLI-M4-Fix-Bugs.md)
