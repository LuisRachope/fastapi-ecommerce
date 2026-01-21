import logging

from fastapi import status
from sqlalchemy.exc import SQLAlchemyError

from app.core.databases.database import async_session

logger = logging.getLogger(__name__)

from app.core.exceptions import ApplicationException
from app.domain.entities.order_item_entity import OrderItemEntity
from app.domain.repositories.order_item_repository import OrderItemRepository
from app.infrastructure.converters import OrderItemConverter


class SQLOrderItemRepository(OrderItemRepository):
    def __init__(self):
        self.converter = OrderItemConverter()

    async def create(self, order_item: OrderItemEntity) -> OrderItemEntity:
        """Create a new order item in the database."""
        try:
            logger.info("Criando item de pedido")
            async with async_session() as session:
                orm_obj = self.converter.entity_to_orm(order_item)
                session.add(orm_obj)
                await session.commit()
                await session.refresh(orm_obj)
                result = self.converter.orm_to_entity(orm_obj)
                logger.info(f"Item de pedido criado. ID: {result.order_id}")
                return result
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao criar item de pedido: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao criar item de pedido",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao criar item de pedido: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao criar item de pedido",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
