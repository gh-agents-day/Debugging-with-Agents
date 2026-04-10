"""
Payment Client - Calls the Payment microservice.
"""
import asyncio
import logging
import random
import yaml
from pathlib import Path

logger = logging.getLogger("payment_client")

# Resolve config path from this file's location - works from any working directory
_config_path = Path(__file__).resolve().parent.parent.parent / "config.yaml"
with open(_config_path, encoding="utf-8") as f:
    _config = yaml.safe_load(f)

TIMEOUT = _config["payment_service"]["timeout"]


class PaymentClient:
    async def process_payment(self, user_id: int, amount: float) -> dict:
        logger.info(f"Initiating payment for user_id={user_id} amount={amount}")

        try:
            # Simulate payment gateway latency (external API call ~2-3 seconds)
            await asyncio.sleep(2)

            # --------------------------------------------------
            # BUG 4: Config timeout (1s) is loaded but NEVER enforced.
            # asyncio.wait_for() is not used, so the 1-second config
            # has zero effect. Payment always takes 2s but never times out.
            # --------------------------------------------------

            # Simulate transient payment gateway failures (50% failure rate)
            # --------------------------------------------------
            # BUG 5: No retry logic. Transient failures are permanent.
            # retry_count=0 in config means every gateway hiccup = failed order.
            # --------------------------------------------------
            if random.choice([True, False]):
                raise Exception("Payment gateway error: upstream timeout")

            logger.info(f"Payment successful for user_id={user_id}")
            return {"status": "success", "user_id": user_id, "amount": amount}

        except Exception as e:
            # --------------------------------------------------
            # BUG 6: Exception is caught and NOT re-raised.
            # The task (created in checkout_service.py) fails silently.
            # No retry, no alerting, no dead-letter queue.
            # --------------------------------------------------
            logger.error("Payment processing error")
            return {"status": "error"}
