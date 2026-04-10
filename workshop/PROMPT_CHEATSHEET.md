# Copilot Prompt Cheat Sheet
## Debug with GitHub Copilot Custom Agents — ShopSphere Workshop

> Copy-paste these prompts directly into Copilot Chat or your custom agents.

---

## Log Analysis Prompts

```
Analyze this production log. Identify:
1. All error types present
2. Which requests fail vs. succeed
3. The time pattern of failures
4. What information is MISSING from the logs that would help debugging
```

```
Given these logs, estimate the blast radius:
- What % of users are affected?
- Is this all users, a subset, or random?
- What pattern determines who is affected?
```

```
These logs show a symptom but I need to find the cause. 
List 5 hypotheses for the root cause, ordered by likelihood.
```

---

## Code Tracing Prompts

```
Trace the execution path of this function from the entry point to where 
it could fail. List every external call and every place where an exception 
could be thrown or swallowed.
```

```
What is the contract of this function? 
1. What are valid inputs?
2. What does it return for each input type?
3. What can it return that callers might not handle?
```

```
Is this async code correct? Check for:
- Missing await / unawaited tasks
- Exceptions that won't propagate to caller
- Race conditions from concurrent execution
```

---

## Root Cause Prompts

```
I have a bug where [SYMPTOM]. 
It happens when [CONDITION] but not when [OTHER CONDITION].
Trace through this code and explain exactly why this behavior occurs.
Point to the specific line(s) where the bug lives.
```

```
This function returns [WRONG VALUE] when I pass [INPUT].
What is the simplest explanation for this behavior?
What would I need to change to make it return [CORRECT VALUE]?
```

```
A user reports [SYMPTOM]. This is reproducible with [STEPS].
Walk through the code as if you are processing this request step by step.
Stop at the first place where the behavior deviates from expected.
```

---

## Fix Generation Prompts

```
Fix ONLY the null/None handling on line [N].
Do not refactor. Do not change anything else.
Treat None as 0 (no discount).
Show me the before/after diff.
```

```
The async task on line [N] is not being awaited. 
Fix this so that:
1. The caller waits for completion
2. If the task raises an exception, it is propagated
3. The overall function returns the correct final status
```

```
This catch/except block is swallowing the exception.
Fix it to:
1. Log the full exception with stack trace
2. Include [user_id, amount] in the log message
3. Re-raise the exception so callers know about it
```

---

## Test Generation Prompts

```
Generate a pytest test for this function that covers:
1. The happy path (all inputs valid, no errors)
2. The bug scenario: [describe the bug]
3. Boundary: [describe an edge case]
Use GIVEN/WHEN/THEN naming.
Use mocks for all external service calls.
```

```
I just fixed [DESCRIBE FIX]. 
Write a regression test that:
- Proves the bug no longer exists
- Will catch it immediately if someone reintroduces the bug
Name it: test_<what it tests>_<expected outcome>
```

```
Generate test cases for all combinations of:
- user_id: even, odd, zero, very large
- amount: normal, zero, negative, very large
- discount: 10.0, 0.0, None
Which combinations should succeed? Which should fail gracefully?
```

---

## Agent Design Prompts

```
I want to create a Copilot agent for debugging [SYSTEM].
The agent should always:
1. [YOUR RULE 1]
2. [YOUR RULE 2]
3. [YOUR RULE 3]
It should know that in my system: [KEY ARCHITECTURE FACTS]
Help me write the system prompt for this agent.
```

```
Review this agent prompt and improve it so that:
1. The output is more structured
2. It always includes confidence levels
3. It leads with the most impactful finding
4. It asks clarifying questions when context is insufficient
```

---

## Copilot Comparisons — Good vs. Bad Prompts

### Finding a bug

| Bad | Good |
|-----|------|
| `find the bug` | `In checkout_service.py:28, discount can be None. Explain why this causes a crash and show the fix.` |
| `why is this failing` | `This function returns {"status":"failed"} for user_id=101 but works for user_id=100. Trace why odd/even IDs behave differently.` |

### Generating tests

| Bad | Good |
|-----|------|
| `write tests` | `Write pytest tests for process_checkout() covering: (1) null discount, (2) payment failure, (3) successful checkout. Use AsyncMock for async methods.` |

### Fixing code

| Bad | Good |
|-----|------|
| `fix this` | `Fix only the missing await on line 37. Do not change anything else. Show before/after diff.` |

---

## Quick Reference: ShopSphere Bug Map

| Bug | File | Line | Symptom | Fix |
|-----|------|------|---------|-----|
| Null discount | `checkout_service.py` | ~28 | Crash for odd userIds | `discount = discount or 0.0` |
| Missing await | `checkout_service.py` | ~37 | Payment silently skipped | `result = await payment_task` |
| Swallowed exception | `checkout_service.py` | ~46 | No error context in logs | `logger.error(..., exc_info=True)` |
| Config timeout | `config.yaml` | ~4 | Payments always "timeout" | Change `timeout: 1` to `timeout: 5` |
| No retry | `payment_client.py` | ~22 | 50% random failure rate | Add retry loop with 3 attempts |
