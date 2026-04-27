# CLI-M1 — Reproduce the Incident

## ShopSphere CLI Track · Time: 10 min 
Features: `--autopilot`, `--agent=`, `-p`, `--allow-tool`, `--output-format=json`

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
copilot --agent=reproduce-agent
```
or 
Use `/agent` thens select `ShopSphere Reproduce Agent` from the list.` 

```bash
copilot -sp "Summarise the reproduce-agent definition at .github/agents/reproduce-agent.agent.md in 5 bullet points."
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
```

Then run:
```bash

You are responding to a P0 production incident on the ShopSphere checkout service.

1. Navigate to python-services/checkout-service and install requirements
2. Run: python demo.py
3. Read observability/incident-report.md
4. Read observability/production-logs.txt (first 100 lines)
5. Produce a Symptom Report with:
   - Failure rate observed (percentage)
   - Error types seen (list each unique exception/message)
   - User segments affected (odd/even userId pattern if visible)
   - Estimated blast radius (how many users per minute at peak traffic)
   - Top 3 hypotheses ranked by evidence strength
```
---

## Step 4 — Capture Output as JSON for Downstream Systems

In an enterprise environment, incident reproduction output is often consumed by
ticketing systems, runbooks, or dashboards. Use `--output-format=json` to
capture structured output:

```bash
"Run demo.py and produce the Symptom Report in JSON format with keys: failure_rate, error_types, affected_segments, hypotheses" > incident-symptom-report.json

cat incident-symptom-report.json
```

> **Enterprise use case:** Pipe this JSON directly into your incident management
> system (PagerDuty, Jira, ServiceNow) to auto-populate incident tickets.
  ---

## Checkpoint ✓

- [ ] `demo.py` run confirms the incident is reproducible (failure rate > 40%)
- [ ] Reproduce agent produced a Symptom Report with failure rate, error types, and hypotheses
- [ ] `incident-symptom-report.json` exists (Step 4)

Next: [CLI-M2 Analyze logs](./CLI-M2-Analyse-Logs.md)
