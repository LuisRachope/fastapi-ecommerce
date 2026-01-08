from uuid import UUID
from app.domain.entities.product import ProductEntity
from app.domain.repositories.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products: dict[UUID, ProductEntity] = {}

    async def create(self, product: ProductEntity) -> ProductEntity:
        if product.id in self.products:
            raise ValueError(f"Produto com ID {product.id} já existe")

        self.products[product.id] = product
        return product
    