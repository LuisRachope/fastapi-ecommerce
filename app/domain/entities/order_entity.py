import datetime

from app.domain.entities.order_item_entity import OrderItemEntity


class OrderEntity:
    def __init__(
        self,
        id: int | None = None,
        order_date: datetime = None,
        status: str = None,
        total_amount: float = None,
    ):
        self.id = id or None
        self.order_date = order_date
        self.status = status
        self.total_amount = total_amount


class OrderCompleteEntity(OrderEntity):
    def __init__(
        self,
        id: int | None = None,
        order_date: datetime = None,
        status: str = None,
        total_amount: float = None,
        items: list[OrderItemEntity] = None,
    ):
        super().__init__(id, order_date, status, total_amount)
        self.items: list[OrderItemEntity] = items or []
