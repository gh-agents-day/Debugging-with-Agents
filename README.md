# ShopSphere Platform — Debug with GitHub Copilot Custom Agents

## Objective

A hands-on workshop where you act as an on-call engineer responding to a **P0 production incident** on a live e-commerce platform. You will use GitHub Copilot — Chat, Agent Mode, Custom Agents, and CLI — to trace, diagnose, and fix five real bugs before the morning stand-up.

| | |
|---|---|
| **Duration** | ~45 min (9 mandatory + 2 optional exercises · ~5 min each) |
| **Audience** | Developers (Intermediate / Senior) |
| **Format** | Instructor-led + Hands-on Lab |
| **Stack** | Python FastAPI · Java Spring Boot (reference) |

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

**Mandatory — follow in order (~45 min)**

| # | Exercise | Copilot Feature |
|---|----------|----------------|
| 01 | [Reproduce the Incident](workshop/Exercise-01-Reproduce-the-Incident.md) | — (baseline) |
| 02 | [Analyze Logs with `#file`](workshop/Exercise-02-Analyze-Logs-with-File-Reference.md) | `#file` |
| 04 | [Debug Live Error with `@terminal`](workshop/Exercise-04-Debug-Live-Error-with-Terminal.md) | `@terminal` |
| 05 | [Find All Bugs with `#codebase`](workshop/Exercise-05-Find-All-Bugs-with-Codebase-Search.md) | `#codebase` |
| 07 | [Fix Bug #1 with `#selection`](workshop/Exercise-07-Fix-Null-Crash-with-Selection.md) | `#selection` |
| 08 | [Fix Bugs #2 & #3 with Agent Mode](workshop/Exercise-08-Fix-Async-and-Exceptions-Agent-Mode.md) | Agent mode |
| 09 | [Build Your Debug Agent](workshop/Exercise-09-Build-Your-Debug-Agent.md) | Custom agent (create) |
| 10 | [Run Your Agent on Bugs #4 & #5](workshop/Exercise-10-Run-Your-Agent-Fix-Config-and-Retry.md) | Custom agent (run) |
| 11 | [Generate Tests with CLI](workshop/Exercise-11-Generate-Tests-with-CLI.md) | `gh copilot` CLI |

**Optional — complete if time allows (~10 min)**

| # | Exercise | Copilot Feature |
|---|----------|----------------|
| 03 | [Map Architecture with Chat](workshop/Exercise-03-Map-Architecture-with-Chat.md) | multi-`#file` |
| 06 | [Create Instructions File](workshop/Exercise-06-Create-Instructions-File.md) | `copilot-instructions.md` |

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
