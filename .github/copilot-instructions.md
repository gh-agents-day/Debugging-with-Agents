# GitHub Copilot — Workspace Instructions for ShopSphere Platform

## About This Codebase
This is the **ShopSphere** e-commerce platform monorepo, used for a GitHub Copilot
debugging workshop. It contains intentional production bugs in the checkout flow.

## Project Structure
- `python-services/checkout-service/` — Primary Python FastAPI service (hands-on)
- `java-services/checkout-service/` — Java Spring Boot equivalent (reference)
- `observability/` — Production logs and incident reports
- `workshop/EXERCISES.md` — Workshop exercises
- `.github/copilot-agents/` — Custom Copilot debug agents

## Coding Conventions
- Python: type hints required on all public methods
- Python: use `logger.error(..., exc_info=True)` for exception logging — never swallow
- Python: async functions must `await` all coroutines — never fire-and-forget
- Config values must be validated at startup, not silently ignored

## Known Bugs (Workshop Context)
The following bugs are intentional and are the subject of this workshop:
1. `checkout_service.py`: discount can be None — callers must handle this
2. `checkout_service.py`: payment task is created but not awaited
3. `checkout_service.py`: exceptions are caught but not logged with context
4. `config.yaml`: timeout=1 is too low and not enforced in code
5. `payment_client.py`: no retry logic on transient failures

## Coding Rules (Derived from Known Bug Patterns)
- Always check any value returned from an external call (API, DB, service client) for `None` before using it in arithmetic or string operations, because downstream `TypeError` crashes are silent and affect all callers who receive that value.
- Never use `asyncio.create_task()` without immediately `await`-ing or explicitly managing the returned task, because fire-and-forget tasks fail silently and the caller cannot detect or recover from their failures.
- Always call `logger.error(..., exc_info=True)` inside every `except` block, because logging without `exc_info` discards the stack trace and makes production root-cause analysis nearly impossible.
- Always enforce config values (e.g., timeouts) at the call site using constructs like `asyncio.wait_for()`, because reading a value from config without using it gives a false sense of safety and leaves the protection completely absent at runtime.
- Never leave `retry_count` at `0` for external service calls without an explicit comment explaining why, because transient failures (network blips, upstream restarts) become permanent failures for users with no recovery path.

## When Helping With This Codebase
- Assume Python 3.12+ and FastAPI patterns
- Prefer minimal, targeted fixes over refactoring
- Always suggest regression tests alongside fixes
- Highlight async/await issues as high priority
- Flag any `except Exception:` blocks that lose error context
