"""
Checkout API — REST endpoint definitions
"""
from fastapi import APIRouter
from app.models.checkout_models import CheckoutRequest, CheckoutResponse
from app.service.checkout_service import CheckoutService

router = APIRouter()
_service = CheckoutService()


@router.post("/checkout", response_model=CheckoutResponse)
async def checkout(request: CheckoutRequest):
    """
    Process a customer checkout.

    This endpoint orchestrates:
    1. Discount calculation
    2. Payment processing
    3. Order confirmation
    """
    return await _service.process_checkout(request.user_id, request.amount)
