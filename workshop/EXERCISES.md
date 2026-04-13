# Workshop Exercises — Debug with GitHub Copilot Custom Agents
## ShopSphere Platform · 4 Core + 9 Optional Exercises

---

## How to Use This Guide

Each exercise:
- Has a **single focused objective** and covers **one Copilot feature**
- Has **copy-paste prompts** — use them in the Chat pane OR the terminal CLI
- Ends with a **checkpoint** to confirm you succeeded
- Builds on the previous exercise

**After each code fix:** run `python demo.py` to see the failure rate drop toward 0%.

**Start here:** run the incident simulator first

```bash
cd python-services/checkout-service
pip install -r requirements.txt
python demo.py
```

---

## Exercise Index

### CORE — Custom Agent Path (~45 min · 4 exercises)
Build and use a custom Copilot agent for each stage of an incident response.
Complete these in order.

| # | Exercise | Agent Created | Objective |
|---|----------|---------------|-----------|
| M1 | [Reproduce the Bug with an Agent](Exercise-M1-Reproduce-Bug-with-Agent.md) | `reproduce-agent` | Run incident simulator + produce Symptom Report |
| M2 | [Analyse Bugs with Logs using an Agent](Exercise-M2-Analyse-Logs-with-Agent.md) | `log-analysis-agent` | Turn raw logs into a ranked Bug Inventory |
| M3 | [Root Cause Analysis with a Custom Agent](Exercise-M3-Root-Cause-Analysis-with-Agent.md) | `root-cause-agent` | Trace backward from symptom to exact code origin |
| M4 | [Fix All Bugs with a Custom Agent](Exercise-M4-Fix-Bugs-with-Agent.md) | `bug-fix-agent` | Apply all 5 minimal fixes via agent with guardrails |
| M5 | [Generate Tests with Agent and CLI](Exercise-M5-Generate-Tests-with-Agent-and-CLI.md) | `test-generator-agent` | Full regression suite · `gh copilot` CLI scaffolding · green run |

### OPTIONAL — Chat Participant Techniques (~45 min · 9 exercises)
These exercises show the underlying Copilot Chat features that custom agents
are built on. Complete these if you want to understand what's happening inside
your agents, or if you have time after the core path.

| # | Exercise | Copilot Feature | Objective |
|---|----------|----------------|-----------|
| 01 | [Reproduce the Incident (manual)](Exercise-01-Reproduce-the-Incident.md) | — (baseline) | See all 5 bugs before using AI |
| 02 | [Analyze Logs with `#file`](Exercise-02-Analyze-Logs-with-File-Reference.md) | `#file` | Point Copilot at the log file |
| 03 | [Map Architecture with Chat](Exercise-03-Map-Architecture-with-Chat.md) | multi-`#file` | Build a complete request flow map |
| 04 | [Debug Live Error with `@terminal`](Exercise-04-Debug-Live-Error-with-Terminal.md) | `@terminal` | Read live errors from the terminal |
| 05 | [Find All Bugs with `#codebase`](Exercise-05-Find-All-Bugs-with-Codebase-Search.md) | `#codebase` | Full bug scan, no manual reading |
| 06 | [Create Instructions File](Exercise-06-Create-Instructions-File.md) | `copilot-instructions.md` | Teach Copilot your team's permanent rules |
| 07 | [Fix Bug #1 with `#selection`](Exercise-07-Fix-Null-Crash-with-Selection.md) | `#selection` | Fix null discount crash |
| 08 | [Fix Bugs #2 & #3 with Agent Mode](Exercise-08-Fix-Async-and-Exceptions-Agent-Mode.md) | Agent mode | Multi-file fix: await + exc_info |
| 09–10 | [Build & Run Your Own Debug Agent](Exercise-09-Build-Your-Debug-Agent.md) | Custom agent | Create and invoke the oncall-agent |
| 11 | [Generate Tests with CLI](Exercise-11-Generate-Tests-with-CLI.md) | `gh copilot` CLI | Write regression tests — lock in the fixes |

---

## Custom Agents Reference

| Agent File | Agent Name | Purpose |
|-----------|-----------|---------|
| `.github/agents/reproduce-agent.agent.md` | ShopSphere Reproduce Agent | Runs simulator, reads incident report, produces Symptom Report |
| `.github/agents/log-analysis-agent.agent.md` | ShopSphere Log Analysis Agent | Reads logs + code, produces ranked Bug Inventory |
| `.github/agents/root-cause-agent.agent.md` | Root Cause Agent | Traces backward from symptom to exact code origin with evidence |
| `.github/agents/bug-fix-agent.agent.md` | ShopSphere Bug Fix Agent | Applies minimal safe fixes with before/after diffs |
| `.github/agents/test-generator-agent.agent.md` | Test Generator Agent | Generates GIVEN/WHEN/THEN regression tests |
| `.github/agents/oncall-agent.agent.md` | ShopSphere On-Call Agent | First-responder triage for production incidents |
| `.github/agents/debug-agent.agent.md` | ShopSphere Debug Agent | Structured root cause analysis from logs + code |

---

## Copilot Chat Participants Reference

| Feature | How to Use |
|---------|-----------|
| `#file:path` | In Chat: attach any file inline |
| `@terminal` | In Chat: read last terminal output |
| `#codebase` | In Chat: search across all workspace files |
| `#selection` | Select code in editor → Chat → type `#selection` |
| Instructions file | `.github/copilot-instructions.md` — auto-loaded into every session |
| Agent mode | Chat mode selector → Agent |
| Custom agents | `.github/agents/*.agent.md` |
| CLI | `gh copilot explain` / `gh copilot suggest` |

---

## Bug Map

| # | Bug | File | Symptom |
|---|-----|------|---------|
| 1 | None discount in arithmetic | `checkout_service.py` | Crash for odd userIds |
| 2 | create_task() not awaited | `checkout_service.py` | Silent payment failures |
| 3 | Exception swallowed — no context | `checkout_service.py` | Useless error logs |
| 4 | Timeout loaded but not enforced | `payment_client.py` + `config.yaml` | Timeouts never fire |
| 5 | No retry on transient failures | `payment_client.py` | 50% random failures |
