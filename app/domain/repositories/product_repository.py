from abc import ABC, abstractmethod

from app.domain.entities.product_entity import ProductEntity


class ProductRepository(ABC):
    @abstractmethod
    async def create(self, product: ProductEntity) -> ProductEntity:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 10) -> list[ProductEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: str) -> ProductEntity | None:
        pass

    @abstractmethod
    async def update(self, product: ProductEntity) -> ProductEntity:
        pass

    @abstractmethod
    async def delete_by_id(self, product_id: str) -> None:
        pass
