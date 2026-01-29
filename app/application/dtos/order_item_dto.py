from pydantic import BaseModel, field_validator


class OrderItemDTO(BaseModel):
    product_id: int
    quantity: int
    price: float

    @field_validator("product_id")
    @classmethod
    def validate_product_id(cls, v):
        if v <= 0:
            raise ValueError("product_id deve ser maior que zero")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("quantity deve ser maior que zero")
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("price deve ser maior que zero")
        return v

    class Config:
        from_attributes = True


class OrderItemResponseDTO(BaseModel):
    id: int
    product_id: int
    order_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True
