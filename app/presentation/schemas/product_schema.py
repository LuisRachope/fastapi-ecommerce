from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class CreateProductInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Nome do produto")
    description: str = Field(..., min_length=1, max_length=1000, description="Descrição do produto")
    price: Annotated[Decimal, Field(..., gt=0, description="Preço do produto")]
    quantity: int = Field(..., ge=0, description="Quantidade em estoque")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Notebook",
                "description": "Notebook de alta performance",
                "price": 3999.99,
                "quantity": 10,
            }
        }


class ProductOutput(BaseModel):
    id: UUID
    name: str
    description: str
    price: Decimal
    quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Notebook",
                "description": "Notebook de alta performance",
                "price": 3999.99,
                "quantity": 10,
                "created_at": "2025-01-07T10:30:00",
                "updated_at": "2025-01-07T10:30:00",
            }
        }


class ProductListOutput(BaseModel):
    total: int
    skip: int
    limit: int
    products: list[ProductOutput]


class UpdateProductInput(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255, description="Nome do produto")
    description: str | None = Field(
        None, min_length=1, max_length=1000, description="Descrição do produto"
    )
    price: Annotated[Decimal | None, Field(None, gt=0, description="Preço do produto")]
    quantity: int | None = Field(None, ge=0, description="Quantidade em estoque")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Notebook",
                "description": "Notebook de alta performance",
                "price": 3999.99,
                "quantity": 10,
            }
        }
