# ShopSphere Platform — Debug with GitHub Copilot Custom Agents

## Objective

A hands-on workshop where you act as an on-call engineer responding to a **P0 production incident** on a live e-commerce platform. You will **build custom Copilot agents** for each stage of the incident response — reproduce, analyse, fix, and validate — and use them to resolve five real production bugs.

| | |
|---|---|
| **Duration** | ~55 min (5 core exercises · ~10 min each) |
| **Audience** | Developers (Intermediate / Senior) |
| **Format** |Hands-on Lab |
| **Stack** | Python FastAPI |

---

## Prerequisites

- GitHub Copilot license (Chat + Agent Mode enabled)
- Python 3.12+ installed
- `gh` CLI installed and authenticated (`gh auth login`)
- VS Code with the GitHub Copilot extension

```bash
cd python-services/checkout-service
pip install -r requirements.txt
python demo.py          # confirm the incident is reproducible
```

---

## Table of Contents

### Core Exercises — Custom Agent Path (~45 min)

Build a custom agent for each stage of an incident response, then use it.

| # | Exercise | Agent You Build | What It Does |
|---|----------|----------------|--------------|
| M1 | [Reproduce the Bug with an Agent](workshop/Exercise-M1-Reproduce-Bug-with-Agent.md) | `reproduce-agent` | Runs simulator · reads incident report · produces Symptom Report |
| M2 | [Analyse Bugs with Logs using an Agent](workshop/Exercise-M2-Analyse-Logs-with-Agent.md) | `log-analysis-agent` | Reads logs · cross-references code · produces Bug Inventory |
| M3 | [Root Cause Analysis with a Custom Agent](workshop/Exercise-M3-Root-Cause-Analysis-with-Agent.md) | `root-cause-agent` | Traces backward from symptom to exact code origin with evidence |
| M4 | [Fix All Bugs with a Custom Agent](workshop/Exercise-M4-Fix-Bugs-with-Agent.md) | `bug-fix-agent` | Applies all 5 minimal fixes with before/after diffs |
| M5 | [Generate Tests with Agent and CLI](workshop/Exercise-M5-Generate-Tests-with-Agent-and-CLI.md) | `test-generator-agent` | Full regression suite · `gh copilot` CLI scaffolding · green run |

### Optional Exercises — Chat Participant Techniques (~45 min)

These exercises cover the Copilot Chat features (`#file`, `@terminal`, `#codebase`,
`#selection`, agent mode) that underpin the custom agents above. Complete these
if you want to understand the building blocks, or if you have time after the core path.

| # | Exercise | Copilot Feature |
|---|----------|----------------|
| 01 | [Reproduce the Incident (manual)](workshop/Exercise-01-Reproduce-the-Incident.md) | — (baseline) |
| 02 | [Analyze Logs with `#file`](workshop/Exercise-02-Analyze-Logs-with-File-Reference.md) | `#file` |
| 03 | [Map Architecture with Chat](workshop/Exercise-03-Map-Architecture-with-Chat.md) | multi-`#file` |
| 04 | [Debug Live Error with `@terminal`](workshop/Exercise-04-Debug-Live-Error-with-Terminal.md) | `@terminal` |
| 05 | [Find All Bugs with `#codebase`](workshop/Exercise-05-Find-All-Bugs-with-Codebase-Search.md) | `#codebase` |
| 06 | [Create Instructions File](workshop/Exercise-06-Create-Instructions-File.md) | `copilot-instructions.md` |
| 07 | [Fix Bug #1 with `#selection`](workshop/Exercise-07-Fix-Null-Crash-with-Selection.md) | `#selection` |
| 08 | [Fix Bugs #2 & #3 with Agent Mode](workshop/Exercise-08-Fix-Async-and-Exceptions-Agent-Mode.md) | Agent mode |
| 09–10 | [Build & Run Your Own Debug Agent](workshop/Exercise-09-Build-Your-Debug-Agent.md) | Custom agent |
| 11 | [Generate Tests with CLI](workshop/Exercise-11-Generate-Tests-with-CLI.md) | `gh copilot` CLI |

> Full exercise details and copy-paste prompts: [`workshop/EXERCISES.md`](workshop/EXERCISES.md)

---

## Bugs in the Code

Five intentional bugs are hidden across the checkout service. Your job is to find and fix all of them.

| # | Bug | File | Symptom |
|---|-----|------|---------|
| 1 | `discount` can be `None` — no null guard | `checkout_service.py` | `TypeError` crash for ~50% of users |
| 2 | `asyncio.create_task()` never awaited | `checkout_service.py` | Silent payment failures |
| 3 | Exception caught but not logged with context | `checkout_service.py` | Errors swallowed — useless logs |
| 4 | Timeout set to `1s` in config, never enforced in code | `payment_client.py` + `config.yaml` | Timeouts never fire |
| 5 | No retry on transient payment failures | `payment_client.py` | 50% random payment errors |

---

## Custom Agents in This Workshop

Six ready-to-use agents live in `.github/agents/`. The core exercises guide
you through building four of them from scratch.

| Agent | File | Built in |
|-------|------|----------|
| ShopSphere Reproduce Agent | `reproduce-agent.agent.md` | Exercise M1 |
| ShopSphere Log Analysis Agent | `log-analysis-agent.agent.md` | Exercise M2 |
| Root Cause Agent | `root-cause-agent.agent.md` | Exercise M3 |
| ShopSphere Bug Fix Agent | `bug-fix-agent.agent.md` | Exercise M4 |
| Test Generator Agent | `test-generator-agent.agent.md` | Exercise M5 |
| ShopSphere On-Call Agent | `oncall-agent.agent.md` | Optional (Exercise 09) |
| ShopSphere Debug Agent | `debug-agent.agent.md` | Reference |

---

## Project Structure

```
.github/
  agents/                    ← Custom Copilot agents (core of this workshop)
  copilot-instructions.md    ← Auto-loaded Copilot context
python-services/
  checkout-service/
    app/service/             ← checkout_service.py (bugs #1, #2, #3 here)
    app/client/              ← payment_client.py (bugs #4, #5 here)
    config.yaml              ← timeout: 1 (bug #4)
    demo.py                  ← incident simulator
observability/
  incident-report.md         ← P0 alert and stack traces
  production-logs.txt        ← raw server logs from the incident window
workshop/                    ← exercise documents
solution/                    ← reference fixes (read after completing exercises)
```
