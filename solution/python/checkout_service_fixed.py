"""
SOLUTION: Fixed CheckoutService — Python
All 5 bugs resolved.
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

            # FIX 1: Handle None discount — treat as 0 (no discount)
            discount = discount if discount is not None else 0.0

            final_amount = amount - discount
            logger.info(f"Discount applied: {discount}. Final amount: {final_amount}")

            # FIX 2: Await the payment task — propagate failures to caller
            payment_result = await self.payment_client.process_payment(user_id, final_amount)

            if payment_result.get("status") != "success":
                logger.error(
                    f"Payment failed for user_id={user_id} amount={final_amount}: {payment_result}"
                )
                return {"status": "failed", "reason": "payment_declined"}

            return {
                "status": "success",
                "user_id": user_id,
                "amount": final_amount,
                "discount_applied": discount,
                "transaction_id": payment_result.get("transaction_id"),
            }

        except Exception as e:
            # FIX 3: Log exception with full context and stack trace
            logger.error(
                f"Checkout failed for user_id={user_id} amount={amount}: {e}",
                exc_info=True,
            )
            return {"status": "failed", "reason": str(e)}
