from uuid import UUID
from datetime import datetime
from decimal import Decimal

class CreateProductDTO:
    def __init__(
        self,
        name: str,
        description: str,
        price: Decimal,
        quantity: int,
    ):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class ProductResponseDTO:
    def __init__(
        self,
        id: UUID,
        name: str,
        description: str,
        price: Decimal,
        quantity: int,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
