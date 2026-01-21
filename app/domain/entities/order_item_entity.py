class OrderItemEntity:
    def __init__(
        self,
        id: int | None = None,
        product_id: int | None = None,
        order_id: int | None = None,
        quantity: int = None,
        price: float = None,
    ):
        self.id = id or None
        self.product_id = product_id or None
        self.order_id = order_id or None
        self.quantity = quantity
        self.price = price
