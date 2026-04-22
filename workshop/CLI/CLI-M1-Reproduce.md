# CLI-M1 — Reproduce the Incident

## ShopSphere CLI Track · Time: 10 min · Features: `--autopilot`, `--agent=`, `-p`, `--allow-tool`, `--output-format=json`

> **CORE EXERCISE** — Use the CLI to autonomously reproduce the P0 production
> incident, then capture the structured output for hand-off to the analysis stage.

---

## Objective

Use `copilot --autopilot` with the custom `reproduce-agent` to:

1. Execute the incident simulator (`demo.py`) autonomously
2. Read the incident report and production logs
3. Produce a structured **Symptom Report** without manual prompting
4. Capture the output as JSON for downstream tooling

---

## Why Autopilot for Reproduction?

In a real incident, reproduction is a race against time. Autopilot mode (`--autopilot`)
lets Copilot execute multi-step tasks without pausing for permission on every tool
call. Combined with `--allow-tool` guards, you get speed _and_ safety: it can run
Python and read files, but cannot touch git or `.env`.

---

## Step 1 — Understand the Reproduce Agent

The `reproduce-agent` lives at `.github/agents/reproduce-agent.agent.md`.
Inspect it from the CLI before running:

```bash
copilot --agent=explore -sp "Summarise the reproduce-agent definition at .github/agents/reproduce-agent.agent.md in 5 bullet points."
```

This uses the built-in **`explore`** agent (fast, read-only) to describe the agent
file without starting a full session. You now know exactly what the agent will do.

---

## Step 2 — Reproduce Interactively First

Before going autonomous, run the simulation manually to understand the baseline:

```bash
cd python-services/checkout-service
pip install -r requirements.txt -q
python demo.py
```

You should see failures. Note the failure rate. This is the incident you are resolving.

---

## Step 3 — Run the Reproduce Agent via CLI (Autopilot)

Now let Copilot reproduce the incident autonomously:

```bash
cd path/to/Debugging-with-Agents

copilot \
  --agent=reproduce-agent \
  --autopilot \
  --allow-tool='shell(python:*)' \
  --allow-tool='shell(pip:*)' \
  --allow-tool='read' \
  --deny-tool='shell(git:*)' \
  -p "You are responding to a P0 production incident on the ShopSphere checkout service.

1. Navigate to python-services/checkout-service and install requirements
2. Run: python demo.py
3. Read observability/incident-report.md
4. Read observability/production-logs.txt (first 100 lines)
5. Produce a Symptom Report with:
   - Failure rate observed (percentage)
   - Error types seen (list each unique exception/message)
   - User segments affected (odd/even userId pattern if visible)
   - Estimated blast radius (how many users per minute at peak traffic)
   - Top 3 hypotheses ranked by evidence strength"
```

**Key flags explained:**

| Flag | Purpose |
|------|---------|
| `--agent=reproduce-agent` | Uses your custom agent's system prompt |
| `--autopilot` | Continues without pausing for each tool permission |
| `--allow-tool='shell(python:*)'` | Pre-authorises Python execution |
| `--deny-tool='shell(git:*)'` | Blocks all git commands — no accidents |
| `-p "..."` | Non-interactive: exits when complete |

---

## Step 4 — Capture Output as JSON for Downstream Systems

In an enterprise environment, incident reproduction output is often consumed by
ticketing systems, runbooks, or dashboards. Use `--output-format=json` to
capture structured output:

```bash
copilot \
  --agent=reproduce-agent \
  --autopilot \
  --allow-tool='shell(python:*)' \
  --allow-tool='read' \
  --deny-tool='shell(git:*)' \
  --output-format=json \
  --silent \
  -p "Run demo.py and produce the Symptom Report in JSON format with keys: failure_rate, error_types, affected_segments, hypotheses" \
  > incident-symptom-report.json

cat incident-symptom-report.json
```

> **Enterprise use case:** Pipe this JSON directly into your incident management
> system (PagerDuty, Jira, ServiceNow) to auto-populate incident tickets.

---

## Step 5 — Save the Session Transcript

Incident response requires audit trails. Save the full session:

```bash
copilot \
  --agent=reproduce-agent \
  --autopilot \
  --allow-tool='shell(python:*)' \
  --allow-tool='read' \
  --deny-tool='shell(git:*)' \
  --share=./observability/cli-reproduce-session.md \
  -p "Reproduce the P0 incident and produce the Symptom Report."
```

The `--share` flag writes a full Markdown transcript of the session to
`./observability/cli-reproduce-session.md`. This becomes part of the incident record.

---

## Step 6 — Re-run with Higher Reasoning Effort

If the Symptom Report is missing nuance (e.g., does not identify the odd/even
userId pattern), increase the reasoning effort:

```bash
copilot \
  --agent=reproduce-agent \
  --autopilot \
  --effort=high \
  --allow-tool='shell(python:*)' \
  --allow-tool='read' \
  --deny-tool='shell(git:*)' \
  -p "Re-run the reproduction. The previous run missed the userId pattern in the failures.
Read demo.py carefully — there may be a statistical pattern in which users fail.
Include it in the Symptom Report."
```

`--effort=high` triggers extended reasoning, useful when a problem requires
deeper analysis than a single-pass response.

---

## Step 7 — Validate in CI (Non-Interactive Scripting)

This pattern is used in CI pipelines to automatically reproduce failures on every
deployment:

```bash
#!/bin/bash
# ci-reproduce.sh — run in CI to confirm checkout health

RESULT=$(copilot \
  --agent=task \
  --autopilot \
  --allow-all-tools \
  --silent \
  -p "Run python demo.py in python-services/checkout-service and output ONLY the failure rate as a decimal (e.g. 0.45). Nothing else.")

echo "Failure rate: $RESULT"

# Fail the CI job if failure rate > 5%
python3 -c "exit(0 if float('$RESULT') < 0.05 else 1)"
```

The built-in **`task`** agent is optimised for command execution — it returns
brief summaries on success and full output on failure, ideal for CI.

---

## Checkpoint ✓

- [ ] `demo.py` run confirms the incident is reproducible (failure rate > 40%)
- [ ] Reproduce agent produced a Symptom Report with failure rate, error types, and hypotheses
- [ ] `incident-symptom-report.json` exists (Step 4)
- [ ] Session transcript saved in `observability/` (Step 5)
- [ ] You can explain the difference between `--autopilot` and interactive mode

**You are ready for CLI-M2.**
