from datetime import datetime
from decimal import Decimal


class ProductEntity:
    def __init__(
        self,
        name: str,
        description: str,
        price: Decimal,
        quantity: int,
        id: int | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
