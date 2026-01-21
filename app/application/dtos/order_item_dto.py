from pydantic import BaseModel


class OrderItemDTO(BaseModel):
    product_id: str
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderItemResponseDTO(BaseModel):
    id: int
    product_id: str
    order_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True
