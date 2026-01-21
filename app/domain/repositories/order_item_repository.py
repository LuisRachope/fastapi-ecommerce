from abc import ABC, abstractmethod

from app.domain.entities.order_item_entity import OrderItemEntity


class OrderItemRepository(ABC):
    @abstractmethod
    async def create(self, order_item: OrderItemEntity) -> OrderItemEntity:
        pass
