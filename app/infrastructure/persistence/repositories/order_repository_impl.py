import logging
from typing import List

from fastapi import status

from app.core.exceptions import ApplicationException

from app.domain.entities.order_entity import OrderEntity
from app.domain.repositories.order_repository import OrderRepository
from app.infrastructure.converters import OrderConverter

from app.core.databases.database import async_session
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)



class SQLOrderRepository(OrderRepository):
    """SQLAlchemy async repository implementation for orders."""

    def __init__(self):
        self.converter = OrderConverter()

    async def create(self, order: OrderEntity) -> OrderEntity:
        """Create a new order in the database."""
        try:
            logger.info(f"Criando pedido")
            async with async_session() as session:
                orm_obj = self.converter.entity_to_orm(order)
                session.add(orm_obj)
                await session.commit()
                await session.refresh(orm_obj)
                result = self.converter.orm_to_entity(orm_obj)
                logger.info(f"Pedido criado. ID: {result.id}")
                return result
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao criar pedido: {str(e)}", exc_info=True)
            raise ApplicationException(message="Erro BD ao criar pedido", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Erro interno ao criar pedido: {str(e)}", exc_info=True)
            raise ApplicationException(message="Erro interno ao criar pedido", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)