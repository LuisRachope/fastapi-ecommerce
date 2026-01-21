from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.application.dtos.order_item_dto import OrderItemDTO, OrderItemResponseDTO


class OrderDTO(BaseModel):
    order_date: datetime
    status: str
    total_amount: float
    items: Optional[list[OrderItemDTO]] = None

    class Config:
        from_attributes = True


class OrderResponseDTO(BaseModel):
    id: int
    order_date: datetime
    status: str
    total_amount: float
    items: Optional[list[OrderItemResponseDTO]] = None

    class Config:
        from_attributes = True