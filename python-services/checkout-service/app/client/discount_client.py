"""
Discount Client - Calls the Discount microservice.
"""
import logging

logger = logging.getLogger("discount_client")

# Simulated discount rules (in production this calls discount-service API)
DISCOUNT_TABLE = {
    # Only even user IDs have a discount configured
    # Odd user IDs return None — discount service returns HTTP 204 No Content
}


class DiscountClient:
    def get_discount(self, user_id: int):
        """
        Returns discount amount for a user.

        Returns:
            float: Discount amount
            None:  If user has no discount (odd user IDs, new accounts)

        KNOWN ISSUE: Returns None when no discount applies.
            Callers MUST handle None return value.
            See: JIRA-4821 - Discount service contract not documented
        """
        if user_id % 2 == 0:
            logger.info(f"Discount found for user_id={user_id}: 10.0")
            return 10.0

        # --------------------------------------------------
        # BUG: Returns None for odd user IDs (new customers, most B2B accounts).
        # The contract says "return 0 if no discount", but this returns None.
        # Checkout service does NOT check for None before doing arithmetic.
        # Result: 50% of users get a TypeError crash -> "status: failed"
        # --------------------------------------------------
        logger.info(f"No discount for user_id={user_id}")
        return None
