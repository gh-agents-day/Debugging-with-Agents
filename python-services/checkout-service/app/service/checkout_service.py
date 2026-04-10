"""
Checkout Service - Core business logic layer.
Orchestrates the discount -> payment -> confirmation flow.
"""
import asyncio
import logging

from app.client.discount_client import DiscountClient
from app.client.payment_client import PaymentClient

logger = logging.getLogger("checkout_service")


class CheckoutService:
    def __init__(self):
        self.payment_client = PaymentClient()
        self.discount_client = DiscountClient()

    async def process_checkout(self, user_id: int, amount: float) -> dict:
        logger.info(f"Processing checkout for user_id={user_id} amount={amount}")

        try:
            # Step 1: Apply discount
            discount = self.discount_client.get_discount(user_id)

            # --------------------------------------------------
            # BUG 1: No null/None check on discount.
            # If user_id is odd, discount_client returns None.
            # This raises: TypeError: unsupported operand type(s)
            # for -: 'float' and 'NoneType'
            # --------------------------------------------------
            final_amount = amount - discount

            logger.info(f"Discount applied: {discount}. Final amount: {final_amount}")

            # Step 2: Process payment
            # --------------------------------------------------
            # BUG 2: asyncio.create_task() starts the coroutine
            # but the result is NEVER awaited. This means:
            # - The method returns before payment completes
            # - Payment failures are completely invisible
            # - "processing" is returned even when payment fails
            # --------------------------------------------------
            payment_task = asyncio.create_task(
                self.payment_client.process_payment(user_id, final_amount)
            )

            # Step 3: Return immediately without waiting for payment
            return {
                "status": "processing",
                "user_id": user_id,
                "amount": final_amount,
                "discount_applied": discount,
                "transaction_id": f"TXN-{user_id}-PENDING",
            }

        except Exception:
            # --------------------------------------------------
            # BUG 3: Exception is swallowed - no error details logged.
            # Developers see "failed" but have zero context about why.
            # This makes production debugging nearly impossible.
            # --------------------------------------------------
            logger.error("Checkout failed")
            return {"status": "failed"}
