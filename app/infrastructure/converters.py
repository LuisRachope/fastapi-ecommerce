from datetime import datetime

from app.domain.entities.order_entity import OrderCompleteEntity, OrderEntity
from app.domain.entities.order_item_entity import OrderItemEntity
from app.domain.entities.product_entity import ProductEntity
from app.domain.entities.user_entity import UserEntity
from app.infrastructure.persistence.models.order_item_orm_model import OrderItemORM
from app.infrastructure.persistence.models.order_orm_model import OrderORM
from app.infrastructure.persistence.models.product_orm_model import ProductORM
from app.infrastructure.persistence.models.user_orm_model import UserORM


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
            id=entity.id,
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

    @staticmethod
    def orm_to_complete_entity(orm: OrderORM) -> OrderCompleteEntity:
        items = [OrderItemConverter.orm_to_entity(item_orm) for item_orm in orm.order_items]
        order_entity = OrderCompleteEntity(
            id=orm.id,
            order_date=orm.order_date,
            status=orm.status,
            total_amount=orm.total_amount,
        )
        order_entity.items = items
        return order_entity


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


class UserConverter:
    @staticmethod
    def orm_to_entity(orm) -> UserEntity:
        return UserEntity(
            id=orm.id,
            email=orm.email,
            hashed_password=orm.hashed_password,
            full_name=orm.full_name,
            is_active=orm.is_active,
            is_superuser=orm.is_superuser,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def entity_to_orm(entity: UserEntity):
        return UserORM(
            id=entity.id,
            email=entity.email,
            hashed_password=entity.hashed_password,
            full_name=entity.full_name,
            is_active=entity.is_active,
            is_superuser=entity.is_superuser,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
