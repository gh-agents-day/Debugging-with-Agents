# ShopSphere CLI Track — Debug an Incident Using GitHub Copilot CLI

## About This Track

The CLI Track runs the **same P0 production incident** as the Core Agent Track, but
everything happens in the terminal using the new **GitHub Copilot CLI**. No VS Code
Chat pane. No mouse. Pure terminal-native AI engineering.

This track is designed for engineers who:
- Work primarily in headless or SSH environments
- Want to integrate AI assistance into CI/CD pipelines and scripts
- Need to enforce security controls over what AI can and cannot do
- Are exploring autonomous and parallel AI workflows

---

## How the CLI Track Relates to the Core Track

| Core Track (VS Code Chat) | CLI Track (Terminal)          | What's the same                    |
| ------------------------- | ----------------------------- | ---------------------------------- |
| M1 — Reproduce (agent)    | CLI-M1 — Reproduce            | Same `reproduce-agent`, same bugs  |
| M2 — Analyse Logs (agent) | CLI-M2 — Analyse Logs         | Same logs, built-in `explore` agent|
| M3 — Root Cause (agent)   | CLI-M3 — Root Cause           | Same root-cause analysis           |
| M4 — Fix Bugs (agent)     | CLI-M4 — Fix Bugs             | Same 5 fixes, `/fleet` parallelism |
| M5 — Tests + CLI          | CLI-M5 — Tests, Review & PR   | Adds `/review`, `/delegate`, `/pr` |

**New in CLI Track:** guardrails with hooks, parallel `/fleet` execution, plan
mode, `/research` deep-dive, `/delegate` PR creation, `--output-format=json` for
CI scripting, and lifecycle hooks for governance.

---

## Prerequisites

```bash
# Install
winget install GitHub.Copilot          # Windows
brew install copilot-cli               # macOS / Linux
npm install -g @github/copilot         # Cross-platform (Node.js 22+)

# Verify
copilot version

# Authenticate (one-time)
cd e:\path\to\Debugging-with-Agents
copilot login
```

> You can also authenticate inside an interactive session:
> ```
> copilot
> /login
> ```

---

## Track Exercises

| # | Exercise | Key CLI Features | Time |
|---|----------|-----------------|------|
| CLI-00 | [Setup & Project Initialization](CLI-00-Setup.md) | `copilot init`, `copilot version`, `/instructions`, repo settings | 5 min |
| CLI-M1 | [Reproduce the Incident](CLI-M1-Reproduce.md) | `--autopilot`, `--agent=`, `-p`, `--allow-tool` | 10 min |
| CLI-M2 | [Analyse Logs with Research Agent](CLI-M2-Analyse-Logs.md) | built-in `explore`, `/research`, `@ file`, `/compact`, `/context` | 10 min |
| CLI-M3 | [Root Cause Analysis in Plan Mode](CLI-M3-Root-Cause.md) | `--plan`, `/plan`, `--effort=high`, `--mode=plan` | 10 min |
| CLI-M4 | [Fix All Bugs with Fleet & Guardrails](CLI-M4-Fix-Bugs.md) | `/fleet`, `--autopilot`, `/diff`, `--allow-tool`, `--deny-tool` | 15 min |
| CLI-M5 | [Tests, Code Review & PR Delegation](CLI-M5-Tests-and-PR.md) | `/review`, `/delegate`, `/pr`, `--output-format=json`, `--share` | 10 min |
---

## CLI Quick-Reference Card

### Launch modes

```bash
copilot                            # Interactive session
copilot -p "prompt"                # Non-interactive (exits after response)
copilot -sp "prompt"               # Silent non-interactive (response only)
copilot --plan                     # Interactive, start in plan mode
copilot --autopilot -p "prompt"    # Autonomous multi-step execution
```

### Key slash commands (inside interactive session)

```bash
/init                   # Generate / update copilot-instructions.md
/plan [prompt]          # Build an implementation plan before coding
/review [prompt]        # Run built-in code-review agent
/research TOPIC         # Deep research using GitHub search + web
/diff                   # Show uncommitted changes
/fleet [prompt]         # Run tasks in parallel subagents
/delegate [prompt]      # Apply changes + create a PR on GitHub
/pr [create|fix|auto]   # Manage pull requests
/compact                # Summarise history to free context window
/context                # Show context window token usage
/session                # Show session info and workspace summary
/share [file|gist]      # Export session transcript
/undo                   # Revert last AI-made file change
/instructions           # View loaded custom instructions
@ FILENAME              # Include a file in the next prompt
```

---

For more information, please refer to [Copilot CLI Reference Guide](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)
