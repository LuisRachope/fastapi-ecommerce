from abc import ABC, abstractmethod

from app.domain.entities.order_entity import OrderEntity


class OrderRepository(ABC):
    @abstractmethod
    async def create(self, order: OrderEntity) -> OrderEntity:
        pass

    @abstractmethod
    async def get_all(self) -> list[OrderEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: str) -> OrderEntity | None:
        pass

    @abstractmethod
    async def delete_by_id(self, order_id: str) -> bool:
        pass
