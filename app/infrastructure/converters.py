from datetime import datetime
from app.domain.entities.order_entity import OrderEntity
from app.domain.entities.order_item_entity import OrderItemEntity
from app.domain.entities.product_entity import ProductEntity
from app.infrastructure.persistence.models import ProductORM
from app.infrastructure.persistence.models.order_item_orm_model import OrderItemORM
from app.infrastructure.persistence.models.order_orm_model import OrderORM


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


class OrderConverter:
    @staticmethod
    def orm_to_entity(orm: OrderORM) -> OrderEntity:
        return OrderEntity(
            id=orm.id,
            order_date=orm.order_date,
            status=orm.status,
            total_amount=orm.total_amount,
        )

    @staticmethod
    def entity_to_orm(entity: OrderEntity) -> OrderORM:
        return OrderORM(
            id=entity.id,
            order_date=entity.order_date,
            status=entity.status,
            total_amount=entity.total_amount,
        )
    

class OrderItemConverter:
    @staticmethod
    def orm_to_entity(orm: OrderItemORM) -> OrderItemEntity:
        return OrderItemEntity(
            id=orm.id,
            product_id=orm.product_id,
            order_id=orm.order_id,
            quantity=orm.quantity,
            price=orm.price,
        )

    @staticmethod
    def entity_to_orm(entity: OrderItemEntity):
        return OrderItemORM(
            product_id=entity.product_id,
            order_id=entity.order_id,
            quantity=entity.quantity,
            price=entity.price,
        )