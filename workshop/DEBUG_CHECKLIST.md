# Production Debugging Checklist
## For Use with GitHub Copilot Custom Agents — ShopSphere Workshop

Use this checklist for every production incident. Work top-to-bottom.

---

## Phase 1 — Triage (< 2 minutes)

- [ ] **Read the error message** — exact text, not paraphrase
- [ ] **Identify the affected service** — which service emitted the error?
- [ ] **Estimate blast radius** — all users? subset? intermittent?
- [ ] **Is data integrity at risk?** — double charges? lost orders? corrupted state?
- [ ] **Is there a quick mitigation?** — feature flag, config rollback, rollback deployment

> **Copilot prompt:** "Given this incident report, what's the blast radius and is there an immediate mitigation?"

---

## Phase 2 — Log Analysis (3–5 minutes)

- [ ] **Find the first error** — scroll to the beginning of the failure window
- [ ] **Find the pattern** — does it fail for all requests or specific ones?
- [ ] **Check what's MISSING** — what context should be in the logs but isn't?
- [ ] **Look for timing clues** — is there a delay before failure? A gap in logs?
- [ ] **Find the last successful request** — what was different about it?

> **Copilot prompt:** "Analyze this log. What patterns do you see? What information is missing that would help debugging?"

---

## Phase 3 — Code Tracing (5–10 minutes)

- [ ] **Find the entry point** — which API/endpoint triggered the failure?
- [ ] **Trace downstream calls** — what does this endpoint call?
- [ ] **Check all null/None returns** — does every caller handle None?
- [ ] **Check all async calls** — is every async operation awaited?
- [ ] **Check exception handling** — are exceptions logged with context?
- [ ] **Check config values** — are timeouts, retries, limits realistic?

> **Copilot prompt:** "Trace the execution path of [function]. For each step, check for null handling, async issues, and swallowed exceptions."

---

## Phase 4 — Root Cause Confirmation

- [ ] **State root cause in one sentence**: "The bug is X because Y"
- [ ] **Identify the exact file and line number**
- [ ] **Reproduce the bug with a minimal test case**
- [ ] **Verify the fix eliminates the reproduction**
- [ ] **Check for similar bugs in related code**

> **Copilot prompt:** "I believe the root cause is [X]. Here is the code. Confirm or challenge this hypothesis and point to the exact line."

---

## Phase 5 — Fix Validation

- [ ] **Minimal fix** — change only what's broken, nothing else
- [ ] **Code review** — have Copilot review the fix for side effects
- [ ] **Write regression test** — test must fail before fix, pass after
- [ ] **Run full test suite** — no regressions
- [ ] **Test the specific user/request that was failing**
- [ ] **Verify logs now include proper context**

> **Copilot prompt:** "Review this fix. Are there any edge cases or side effects I've missed? Generate a regression test for the bug I fixed."

---

## Phase 6 — Post-Incident

- [ ] **Document the root cause** — update incident report
- [ ] **Add observability** — ensure this class of bug is detectable via logs/metrics next time
- [ ] **Create follow-up tickets** — for structural improvements (retry, circuit breaker, etc.)
- [ ] **Update your debug agent** — add this bug pattern to your agent's knowledge
- [ ] **Write a blameless postmortem** — share learnings with team

---

## Common Bug Patterns — Quick Reference

| Pattern | How to Spot | Fix |
|---------|------------|-----|
| Null pointer / TypeError | "NullPointerException", "unsupported operand type for NoneType" | Add null check, return default value |
| Missing await | "processing" returned before async completes | Add `await` / `.get()` |
| Swallowed exception | Error message with no stack trace, mystery "failed" | Add `exc_info=True` / `e` to logger.error |
| Bad timeout config | All calls to a service fail consistently | Check config, enforce timeout with asyncio.wait_for / CompletableFuture.get(timeout) |
| No retry | 50%+ failure rate, errors are transient | Add retry with backoff |
| Race condition | Intermittent failures, hard to reproduce | Find shared state, add synchronization |
| Missing correlation ID | Can't trace a request across services | Add trace ID to all log messages |

---

## Copilot Agent Quick-Pick

| Situation | Use This Agent |
|-----------|---------------|
| Have logs, need root cause | `debug-agent` |
| Have a symptom, don't know where to start | `root-cause-agent` |
| Have a fix, need tests | `test-generator-agent` |
| Real incident, need immediate triage | `oncall-agent` (build your own!) |
