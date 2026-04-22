# CLI-00 — Setup & Project Initialization

## ShopSphere CLI Track · Time: 5 min · Features: `copilot init`, `copilot version`, `copilot login`, repo settings

> **START HERE** — Establish the CLI toolchain and configure Copilot to understand
> the ShopSphere codebase before the first incident response step.

---

## Objective

By the end of this exercise you will have:

1. The Copilot CLI installed and authenticated
2. A project-specific `copilot-instructions.md` generated or verified
3. Repository-level CLI settings applied
4. A validated baseline — the CLI reads and understands the codebase

---

## Step 1 — Install the Copilot CLI

Choose the method for your platform:

```bash
# Windows (WinGet)
winget install GitHub.Copilot

# macOS / Linux (Homebrew)
brew install copilot-cli

# Cross-platform (Node.js 22+ required)
npm install -g @github/copilot
```

Verify the installation:

```bash
copilot version
```

Expected output:

```
GitHub Copilot CLI x.y.z
```

> If an update is available, `copilot update` will install the latest version.

---

## Step 2 — Authenticate

Navigate to the workshop project root, then authenticate:

```bash
cd path/to/Debugging-with-Agents
copilot login
```

Follow the device-flow prompts. This stores credentials in your system keychain.
You only need to do this once per machine.

**Verify authentication inside an interactive session:**

```bash
copilot
/user show
```

You should see your GitHub username. Type `/exit` to leave.

---

## Step 3 — Initialize the Project

`copilot init` (or `/init` inside a session) analyses the codebase and writes
`.github/copilot-instructions.md` with project-specific guidance that every
future CLI session loads automatically.

```bash
copilot init
```

This will:
- Scan the project structure and key files
- Detect the Python FastAPI stack
- Identify test frameworks and build commands
- Write structured guidance into `.github/copilot-instructions.md`

> **Note:** The workshop already ships with a `.github/copilot-instructions.md`.
> Running `copilot init` will suggest improvements — review and apply what is relevant.

After init, verify the instructions are loaded:

```bash
copilot
/instructions
```

You should see `.github/copilot-instructions.md` listed as active. Type `/exit`.

---

## Step 4 — Apply Repository CLI Settings

Create a repository-level settings file so everyone on the team gets the same
CLI behaviour:

```bash
mkdir -p .github/copilot
```

Create `.github/copilot/settings.json`:

```json
{
  "companyAnnouncements": [
    "ShopSphere incident response CLI track active. Run /init if instructions are missing."
  ]
}
```

This message is shown at the start of every CLI session in this repository.

---

## Step 5 — Confirm the CLI Understands the Codebase

Run a non-interactive probe to confirm context is loaded correctly:

```bash
copilot -sp "In one sentence, what is the ShopSphere checkout service responsible for?"
```

The response should mention order totals, discounts, and payment processing —
not a generic description. If it doesn't, check that `/instructions` shows
`.github/copilot-instructions.md` as active.

**Enterprise tip — model selection:**

```bash
# Set your preferred model for this session
copilot --model=claude-sonnet-4.5 -sp "Summarise the project structure."

# Or set it permanently via environment variable
export COPILOT_MODEL=claude-sonnet-4.5
```

---

## Step 6 — Set Up a Safe Defaults Session

Before fixing production bugs, configure what the CLI is and is not allowed to
do autonomously. This is the enterprise governance baseline:

```bash
# Start an interactive session that:
# - Cannot push to remote git (safety: no accidental pushes)
# - Cannot access the .env file (security: no credential leaks)
# - CAN run Python and pytest (needed for reproduction and tests)

copilot \
  --allow-tool='shell(python:*)' \
  --allow-tool='shell(pytest:*)' \
  --allow-tool='shell(pip:*)' \
  --deny-tool='shell(git push)' \
  --deny-tool='read(.env)'
```

> These permission flags persist for the lifetime of the session only.
> For persistent governance, use hooks (see CLI-Bonus-Hooks-and-Governance.md).

---

## Checkpoint ✓

- [ ] `copilot version` shows a valid version
- [ ] `copilot login` completed — `copilot /user show` shows your GitHub username
- [ ] `copilot init` has run — `.github/copilot-instructions.md` exists and is non-trivial
- [ ] Non-interactive probe returns a ShopSphere-specific answer
- [ ] `.github/copilot/settings.json` created

Next: [CLI-M1-Reproduce.md](./CLI-M1-Reproduce.md)
