"""
SOLUTION: Fixed PaymentClient — Python
Fixes: timeout enforcement, retry logic, proper exception propagation.
"""
import asyncio
import logging
import random
import yaml
import os

logger = logging.getLogger("payment_client")

_config_path = os.path.join(os.path.dirname(__file__), "../../config.yaml")
with open(_config_path) as f:
    _config = yaml.safe_load(f)

# FIX 4: Read timeout and retry from config
TIMEOUT = _config["payment_service"]["timeout"]
RETRY_COUNT = 3  # FIX 5: Add retry logic


class PaymentClient:
    async def process_payment(self, user_id: int, amount: float) -> dict:
        last_error = None

        # FIX 5: Retry loop
        for attempt in range(1, RETRY_COUNT + 1):
            try:
                logger.info(
                    f"Payment attempt {attempt}/{RETRY_COUNT} for user_id={user_id} amount={amount}"
                )

                # FIX 4: Enforce timeout using asyncio.wait_for
                result = await asyncio.wait_for(
                    self._call_payment_gateway(user_id, amount),
                    timeout=TIMEOUT,
                )

                logger.info(f"Payment successful for user_id={user_id} after {attempt} attempt(s)")
                return {"status": "success", "transaction_id": f"TXN-{user_id}-{attempt}"}

            except asyncio.TimeoutError:
                last_error = f"Payment gateway timeout after {TIMEOUT}s"
                logger.warning(f"Payment timeout on attempt {attempt} for user_id={user_id}")
            except Exception as e:
                last_error = str(e)
                logger.warning(
                    f"Payment error on attempt {attempt} for user_id={user_id}: {e}"
                )

            if attempt < RETRY_COUNT:
                await asyncio.sleep(0.5)

        logger.error(
            f"Payment failed after {RETRY_COUNT} attempts for user_id={user_id}: {last_error}"
        )
        # FIX 6: Return error status instead of silently failing
        return {"status": "error", "reason": last_error}

    async def _call_payment_gateway(self, user_id: int, amount: float) -> dict:
        """Simulates external payment gateway call."""
        await asyncio.sleep(2)
        if random.choice([True, False]):
            raise Exception("Payment gateway error: upstream timeout")
        return {"status": "success"}
