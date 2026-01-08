from abc import ABC, abstractmethod
from app.domain.entities.product import ProductEntity


class ProductRepository(ABC):    
    @abstractmethod
    async def create(self, product: ProductEntity) -> ProductEntity:
        pass
 