# Workshop Exercises — Debug with GitHub Copilot Custom Agents
## ShopSphere Platform · 11 Exercises · ~5 min each

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

### MANDATORY — Core Workshop Path (~45 min · 9 exercises)
Complete these in order. They form the full end-to-end debugging and validation journey.

| # | Exercise | Copilot Feature | Objective |
|---|----------|----------------|-----------|
| 01 | [Reproduce the Incident](Exercise-01-Reproduce-the-Incident.md) | — (baseline) | See all 5 bugs before using AI |
| 02 | [Analyze Logs with `#file`](Exercise-02-Analyze-Logs-with-File-Reference.md) | `#file` | Point Copilot at the log file |
| 04 | [Debug Live Error with `@terminal`](Exercise-04-Debug-Live-Error-with-Terminal.md) | `@terminal` | Read live errors from the terminal |
| 05 | [Find All Bugs with `#codebase`](Exercise-05-Find-All-Bugs-with-Codebase-Search.md) | `#codebase` | Full bug scan, no manual reading |
| 07 | [Fix Bug #1 with `#selection`](Exercise-07-Fix-Null-Crash-with-Selection.md) | `#selection` | Fix null discount crash |
| 08 | [Fix Bugs #2 & #3 with Agent Mode](Exercise-08-Fix-Async-and-Exceptions-Agent-Mode.md) | Agent mode | Multi-file fix: await + exc_info |
| 09 | [Build Your Debug Agent](Exercise-09-Build-Your-Debug-Agent.md) | Custom agent (create) | Create your own oncall-agent |
| 10 | [Run Your Agent on Bugs #4 & #5](Exercise-10-Run-Your-Agent-Fix-Config-and-Retry.md) | Custom agent (run) | Fix timeout + retry via your agent |
| 11 | [Generate Tests with CLI](Exercise-11-Generate-Tests-with-CLI.md) | `gh copilot` CLI | Write regression tests — lock in the fixes |

### OPTIONAL — Go Deeper (~10 min · 2 exercises)
Complete these if time allows, or revisit after the workshop.

| # | Exercise | Copilot Feature | Objective |
|---|----------|----------------|-----------|
| 03 | [Map Architecture with Chat](Exercise-03-Map-Architecture-with-Chat.md) | multi-`#file` | Build a complete request flow map |
| 06 | [Create Instructions File](Exercise-06-Create-Instructions-File.md) | `copilot-instructions.md` | Teach Copilot your team's permanent rules |

---

## Copilot Features Reference

| Feature | How to Use |
|---------|-----------|
| `#file:path` | In Chat: attach any file inline |
| `@terminal` | In Chat: read last terminal output |
| `#codebase` | In Chat: search across all workspace files |
| `#selection` | Select code in editor → Chat → type `#selection` |
| Instructions file | `.github/copilot-instructions.md` — auto-loaded into every session |
| Agent mode | Chat mode selector → Agent |
| Custom agents | `.github/copilot-agents/*.prompt.md` |
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
