"""
Pydantic models for Checkout Service API.
"""
from pydantic import BaseModel, Field
from typing import Optional


class CheckoutRequest(BaseModel):
    user_id: int = Field(..., example=101, description="Unique customer identifier")
    amount: float = Field(..., example=150.00, description="Cart total before discounts")


class CheckoutResponse(BaseModel):
    status: str = Field(..., example="processing")
    user_id: Optional[int] = None
    amount: Optional[float] = None
    discount_applied: Optional[float] = None
    transaction_id: Optional[str] = None
