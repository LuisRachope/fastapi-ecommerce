from enum import Enum


class OrderStatus(str, Enum):
    """Status possíveis para um pedido."""

    PENDING = "Pending"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"

    def __str__(self) -> str:
        return self.value
