from fastapi import status
from fastapi.exceptions import ValidationException

from app.application.dtos.order_dto import OrderDTO, OrderResponseDTO
from app.application.dtos.order_item_dto import OrderItemResponseDTO
from app.core.exceptions import ApplicationException
from app.domain.entities.order_entity import OrderCompleteEntity, OrderEntity
from app.domain.entities.order_item_entity import OrderItemEntity
from app.domain.repositories.order_item_repository import OrderItemRepository
from app.domain.repositories.order_repository import OrderRepository


class OrderService:
    """Service class for managing orders."""

    def __init__(
        self, order_repository: OrderRepository, order_item_repository: OrderItemRepository
    ):
        self.order_repository = order_repository
        self.order_item_repository = order_item_repository

    async def create_order(self, order_data: OrderDTO) -> OrderResponseDTO:
        """Create a new order."""
        try:
            order_entity = OrderEntity(
                order_date=order_data.order_date,
                status=order_data.status,
                total_amount=order_data.total_amount,
            )
            response_order: OrderEntity = await self.order_repository.create(order_entity)

            items_entities = []
            for item in order_data.items:
                order_item_entity = OrderItemEntity(
                    order_id=response_order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                )
                item_entity: OrderItemEntity = await self.order_item_repository.create(
                    order_item_entity
                )
                items_entities.append(item_entity)

            items_dtos = [
                OrderItemResponseDTO(
                    id=item_entity.id,
                    order_id=item_entity.order_id,
                    product_id=item_entity.product_id,
                    quantity=item_entity.quantity,
                    price=item_entity.price,
                )
                for item_entity in items_entities
            ]
            return OrderResponseDTO(
                id=response_order.id,
                order_date=response_order.order_date,
                status=response_order.status,
                total_amount=response_order.total_amount,
                items=items_dtos,
            )
        except ValidationException:
            raise
        except ApplicationException as e:
            raise ApplicationException(status_code=e.status_code, message=e.message)
        except Exception as e:
            raise ApplicationException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)
            )

    async def get_all_orders(self) -> list[OrderResponseDTO]:
        """Retrieve all orders."""
        try:
            orders_entities: list[OrderCompleteEntity] = await self.order_repository.get_all()
            orders_dtos = []
            for order_entity in orders_entities:
                items_dtos = [
                    OrderItemResponseDTO(
                        id=item_entity.id,
                        order_id=item_entity.order_id,
                        product_id=item_entity.product_id,
                        quantity=item_entity.quantity,
                        price=item_entity.price,
                    )
                    for item_entity in order_entity.items
                ]
                order_dto = OrderResponseDTO(
                    id=order_entity.id,
                    order_date=order_entity.order_date,
                    status=order_entity.status,
                    total_amount=order_entity.total_amount,
                    items=items_dtos,
                )
                orders_dtos.append(order_dto)
            return orders_dtos
        except ApplicationException as e:
            raise ApplicationException(message=e.message, status_code=e.status_code)
        except Exception as e:
            raise ApplicationException(
                message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_order_by_id(self, order_id: str) -> bool:
        """Delete an order by its ID."""
        try:
            order = await self.order_repository.get_by_id(order_id)
            if order is None:
                return True
            await self.order_repository.delete_by_id(order_id)
            return True
        except ApplicationException as e:
            raise ApplicationException(status_code=e.status_code, message=e.message)
        except Exception as e:
            raise ApplicationException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)
            )
