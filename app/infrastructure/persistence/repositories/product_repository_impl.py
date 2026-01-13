from typing import List

from app.domain.entities.product import ProductEntity
from app.domain.repositories.product_repository import ProductRepository

from app.infrastructure.database import ProductORM, async_session
from app.infrastructure.converters import ProductConverter
from sqlalchemy import select


class SQLProductRepository(ProductRepository):
    """SQLAlchemy async repository implementation for products."""

    def __init__(self):
        self.converter = ProductConverter()

    async def create(self, product: ProductEntity) -> ProductEntity:
        """Create a new product in the database."""
        async with async_session() as session:
            orm_obj = self.converter.entity_to_orm(product)
            session.add(orm_obj)
            await session.commit()
            await session.refresh(orm_obj)
            return self.converter.orm_to_entity(orm_obj)

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[ProductEntity]:
        """Retrieve all products with pagination."""
        async with async_session() as session:
            stmt = select(ProductORM).offset(skip).limit(limit)
            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [self.converter.orm_to_entity(r) for r in rows]
