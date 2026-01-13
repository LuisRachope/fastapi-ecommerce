from datetime import datetime
from app.domain.entities.product import ProductEntity
from app.infrastructure.database import ProductORM


class ProductConverter:
    @staticmethod
    def orm_to_entity(orm: ProductORM) -> ProductEntity:
        return ProductEntity(
            name=orm.name,
            description=orm.description,
            price=orm.price,
            quantity=orm.quantity,
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def entity_to_orm(entity: ProductEntity) -> ProductORM:
        return ProductORM(
            id=str(entity.id),
            name=entity.name,
            description=entity.description,
            price=entity.price,
            quantity=entity.quantity,
            created_at=entity.created_at or datetime.utcnow(),
            updated_at=entity.updated_at or datetime.utcnow(),
        )
