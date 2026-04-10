"""
ShopSphere Incident Simulator
==============================
Run this script to reproduce the P0 production incident.
Watch checkout fail in real-time — then open workshop/EXERCISES.md to debug it.

Usage:
    cd python-services/checkout-service
    python demo.py
"""
import asyncio
import logging
import sys
import time
from pathlib import Path

# Suppress all logging during demo so the table output stays clean
# (Run `uvicorn main:app --reload` for full logs)
logging.disable(logging.CRITICAL)

# Ensure the service package is importable from this script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.service.checkout_service import CheckoutService

# ─── ANSI colours ──────────────────────────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

# ─── Simulated customer requests (mirrors production traffic pattern) ──────────
TEST_ORDERS = [
    {"user_id": 100, "amount": 150.00, "note": "Regular customer — has discount"},
    {"user_id": 101, "amount":  89.99, "note": "New signup — no discount tier"},
    {"user_id": 102, "amount": 250.00, "note": "Premium member"},
    {"user_id": 103, "amount":  45.00, "note": "Trial user"},
    {"user_id": 104, "amount": 199.99, "note": "Returning customer"},
    {"user_id": 105, "amount":  75.00, "note": "B2B account"},
    {"user_id": 200, "amount": 320.00, "note": "Enterprise client"},
    {"user_id": 201, "amount":  55.00, "note": "Referral user"},
    {"user_id": 300, "amount": 100.00, "note": "VIP member"},
    {"user_id": 301, "amount":  88.00, "note": "First-time buyer"},
]


def banner():
    print(f"""
{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════╗
║          ShopSphere Platform  ·  Checkout Service v2.4.1     ║
║          Incident Simulation — P0 Production Scenario        ║
╚══════════════════════════════════════════════════════════════╝{RESET}""")


def print_alert():
    print(f"""
{BOLD}{RED}  ┌─────────────────────────────────────────────────────────┐
  │  🔔 PagerDuty  [P0]  2026-04-10  02:47 UTC               │
  │                                                           │
  │  ShopSphere Checkout — Failure rate spiking              │
  │  Revenue impact: $12,000 / min                           │
  │  SLA breach in: 8 minutes                                │
  └─────────────────────────────────────────────────────────┘{RESET}
""")


async def run_simulation():
    service = CheckoutService()

    banner()
    print_alert()

    print(f"{BOLD}  Replaying last 10 checkout requests from production...{RESET}\n")
    print(f"  {'USER ID':<10} {'AMOUNT':>10}  {'STATUS':<15}  NOTE")
    print(f"  {DIM}{'─'*65}{RESET}")

    results = []
    for order in TEST_ORDERS:
        await asyncio.sleep(0.15)  # realistic pacing
        try:
            result = await service.process_checkout(order["user_id"], order["amount"])
            status = result.get("status", "unknown")
        except Exception as exc:
            status = "exception"
            result = {"error": str(exc)}

        if status in ("success", "processing"):
            icon  = f"{GREEN}✓{RESET}"
            label = f"{GREEN}{status:<15}{RESET}"
        else:
            icon  = f"{RED}✗{RESET}"
            label = f"{RED}{status:<15}{RESET}"

        print(
            f"  {icon}  user={order['user_id']:<6}  ${order['amount']:>8.2f}  "
            f"{label}  {DIM}{order['note']}{RESET}"
        )
        results.append(status)

    # ── Summary ─────────────────────────────────────────────────────────────────
    total   = len(results)
    failed  = sum(1 for r in results if r not in ("success", "processing"))
    passed  = total - failed
    rate    = (failed / total) * 100

    rate_colour = RED if rate > 20 else YELLOW

    print(f"\n  {DIM}{'─'*65}{RESET}")
    print(f"  Results  →  {GREEN}{passed} passed{RESET}  /  {RED}{failed} failed{RESET}  "
          f"({rate_colour}{rate:.0f}% failure rate{RESET})\n")

    if rate > 20:
        print(f"{BOLD}{RED}  ⚠  INCIDENT ACTIVE — failure rate exceeds 20% SLA threshold{RESET}")
        print(f"\n{BOLD}  What to do next:{RESET}")
        print(f"  {YELLOW}1. Open  workshop/EXERCISES.md{RESET}  — start at Exercise 01")
        print(f"  {YELLOW}2. Open  observability/production-logs.txt{RESET}  — read the logs")
        print(f"  {YELLOW}3. Open  observability/incident-report.md{RESET}  — read the incident report")
        print(f"\n  {DIM}Tip: Run  python demo.py  again after each fix to see improvement.{RESET}\n")
    else:
        print(f"{BOLD}{GREEN}  ✓ All bugs fixed — checkout is healthy!{RESET}\n")


if __name__ == "__main__":
    asyncio.run(run_simulation())
