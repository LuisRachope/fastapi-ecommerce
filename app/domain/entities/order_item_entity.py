

from typing import Optional


class OrderItemEntity:
    def __init__(
            self, 
            id: Optional[int] = None,
            product_id: Optional[int] = None, 
            order_id: Optional[int] = None, 
            quantity: int = None, 
            price: float = None
    ):
        self.id = id or None
        self.product_id = product_id or None
        self.order_id = order_id or None
        self.quantity = quantity
        self.price = price