import logging

from fastapi import status
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.core.databases.database import async_session
from app.core.exceptions import ApplicationException
from app.domain.entities.order_entity import OrderCompleteEntity, OrderEntity
from app.domain.repositories.order_repository import OrderRepository
from app.infrastructure.converters import OrderConverter
from app.infrastructure.persistence.models.order_orm_model import OrderORM

logger = logging.getLogger(__name__)


class SQLOrderRepository(OrderRepository):
    """SQLAlchemy async repository implementation for orders."""

    def __init__(self):
        self.converter = OrderConverter()

    async def create(self, order: OrderEntity) -> OrderEntity:
        """Create a new order in the database."""
        try:
            logger.info("Criando pedido")
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
            raise ApplicationException(
                message="Erro BD ao criar pedido", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Erro interno ao criar pedido: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao criar pedido",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_by_id(self, order_id: str) -> OrderEntity | None:
        """Retrieve an order by its ID."""
        try:
            logger.info(f"Recuperando pedido com ID: {order_id}")
            async with async_session() as session:
                stmt = select(OrderORM).where(OrderORM.id == order_id)
                result = await session.execute(stmt)
                orm_order = result.scalar_one_or_none()

                if orm_order is None:
                    logger.info(f"Pedido com ID {order_id} não encontrado")
                    return None

                entity = self.converter.orm_to_entity(orm_order)
                logger.info(f"Pedido com ID {order_id} recuperado com sucesso")
                return entity
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao recuperar pedido: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao recuperar pedido",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao recuperar pedido: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao recuperar pedido",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_all(self) -> list[OrderCompleteEntity]:
        """Retrieve all orders from the database."""
        try:
            logger.info("Recuperando todos os pedidos")
            async with async_session() as session:
                stmt = select(OrderORM).options(selectinload(OrderORM.order_items))
                result = await session.execute(stmt)
                orm_orders = result.scalars().all()

                entities = [
                    self.converter.orm_to_complete_entity(orm_obj) for orm_obj in orm_orders
                ]
                logger.info(f"{len(entities)} pedidos recuperados com itens")
                result = entities
                return result
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao recuperar pedidos: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao recuperar pedidos",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao recuperar pedidos: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao recuperar pedidos",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def delete_by_id(self, order_id: str) -> bool:
        """Delete an order by its ID."""
        try:
            logger.info(f"Deletando pedido com ID: {order_id}")
            async with async_session() as session:
                stmt = delete(OrderORM).where(OrderORM.id == order_id)
                await session.execute(stmt)
                await session.commit()
                logger.info(f"Pedido com ID {order_id} deletado com sucesso")
                return True
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao deletar pedido: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao deletar pedido",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except ApplicationException:
            raise
        except Exception as e:
            logger.error(f"Erro interno ao deletar pedido: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao deletar pedido",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
