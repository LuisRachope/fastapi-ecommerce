from abc import ABC, abstractmethod

from app.domain.entities.order_entity import OrderEntity


class OrderRepository(ABC):
    @abstractmethod
    async def create(self, order: OrderEntity) -> OrderEntity:
        pass

    @abstractmethod
    async def get_all(self) -> list[OrderEntity]:
        pass
