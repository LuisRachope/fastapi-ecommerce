from datetime import datetime

from pydantic import BaseModel, field_validator

from app.application.dtos.order_item_dto import (
    OrderItemDTO,
    OrderItemInputDTO,
    OrderItemResponseDTO,
)


class OrderDTO(BaseModel):
    items: list[OrderItemDTO]

    @field_validator("items")
    @classmethod
    def validate_items(cls, v):
        if not v or len(v) == 0:
            raise ValueError("A lista de itens não pode estar vazia")
        return v

    class Config:
        from_attributes = True


class OrderInputDTO(BaseModel):
    items: list[OrderItemInputDTO]

    @field_validator("items")
    @classmethod
    def validate_items(cls, v):
        if not v or len(v) == 0:
            raise ValueError("A lista de itens não pode estar vazia")
        return v

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
