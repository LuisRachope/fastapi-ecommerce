from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.product import ProductEntity


class ProductRepository(ABC):    
    @abstractmethod
    async def create(self, product: ProductEntity) -> ProductEntity:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 10) -> List[ProductEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: str) -> ProductEntity | None:
        pass

    @abstractmethod
    async def update(self, product: ProductEntity) -> ProductEntity:
        pass
