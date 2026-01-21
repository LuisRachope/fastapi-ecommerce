from datetime import datetime

from pydantic import BaseModel

from app.application.dtos.order_item_dto import OrderItemDTO, OrderItemResponseDTO


class OrderDTO(BaseModel):
    order_date: datetime
    status: str
    total_amount: float
    items: list[OrderItemDTO] | None = None

    class Config:
        from_attributes = True


class OrderResponseDTO(BaseModel):
    id: int
    order_date: datetime
    status: str
    total_amount: float
    items: list[OrderItemResponseDTO] | None = None

    class Config:
        from_attributes = True
