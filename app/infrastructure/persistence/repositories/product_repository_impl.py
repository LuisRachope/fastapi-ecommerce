import logging

from fastapi import status
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.databases.database import async_session
from app.core.exceptions import ApplicationException
from app.domain.entities.product_entity import ProductEntity
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.converters import ProductConverter
from app.infrastructure.persistence.models import ProductORM

logger = logging.getLogger(__name__)


class SQLProductRepository(ProductRepository):
    """SQLAlchemy async repository implementation for products."""

    def __init__(self):
        self.converter = ProductConverter()

    async def create(self, product: ProductEntity) -> ProductEntity:
        """Create a new product in the database."""
        try:
            logger.info(f"Criando produto: {product.name}")
            async with async_session() as session:
                orm_obj = self.converter.entity_to_orm(product)
                session.add(orm_obj)
                await session.commit()
                await session.refresh(orm_obj)
                result = self.converter.orm_to_entity(orm_obj)
                logger.info(f"Produto criado. ID: {result.id}")
                return result
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao criar produto: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao criar produto",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao criar produto: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao criar produto",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[ProductEntity]:
        """Retrieve all products with pagination."""
        try:
            logger.debug(f"get_all - skip: {skip}, limit: {limit}")
            async with async_session() as session:
                stmt = select(ProductORM).offset(skip).limit(limit)
                result = await session.execute(stmt)
                rows = result.scalars().all()
                logger.info(f"Produtos recuperados: {len(rows)}")
                return [self.converter.orm_to_entity(orm) for orm in rows]
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao recuperar produtos: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao recuperar produtos",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao recuperar produtos: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao recuperar produtos",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_by_id(self, product_id: int) -> ProductEntity | None:
        """Get a product by ID."""
        try:
            logger.debug(f"Buscando produto: {product_id}")
            async with async_session() as session:
                query = select(ProductORM).where(ProductORM.id == product_id)
                result = await session.execute(query)
                orm_obj = result.scalar_one_or_none()
                if orm_obj:
                    logger.info(f"Produto encontrado: {product_id}")
                    return self.converter.orm_to_entity(orm_obj)
                else:
                    logger.warning(f"Produto não encontrado: {product_id}")
                    return None
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao buscar produto {product_id}: {str(e)}", exc_info=True)
            raise ApplicationException(
                message=f"Erro ao buscar produto {product_id}",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Erro interno ao buscar produto {product_id}: {str(e)}", exc_info=True)
            raise ApplicationException(
                message=f"Erro interno ao buscar produto {product_id}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def update(self, product: ProductEntity) -> ProductEntity:
        """Update an existing product in the database."""
        try:
            logger.info(f"Atualizando produto: {product.id}")
            async with async_session() as session:
                orm_obj = self.converter.entity_to_orm(product)
                orm_obj = await session.merge(orm_obj)
                await session.commit()
                await session.refresh(orm_obj)
                result = self.converter.orm_to_entity(orm_obj)

                logger.info(f"Produto atualizado: {result.id}")
                return result
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao atualizar produto {product.id}: {str(e)}", exc_info=True)
            raise ApplicationException(
                message=f"Erro BD ao atualizar produto {product.id}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except ApplicationException:
            raise
        except Exception as e:
            logger.error(f"Erro interno ao atualizar produto {product.id}: {str(e)}", exc_info=True)
            raise ApplicationException(
                message=f"Erro interno ao atualizar produto {product.id}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def delete_by_id(self, product_id: int) -> None:
        """Delete a product by ID."""
        try:
            logger.info(f"Deletando produto: {product_id}")
            async with async_session() as session:
                stmt = delete(ProductORM).where(ProductORM.id == product_id)
                result = await session.execute(stmt)
                await session.commit()
                if result.rowcount > 0:
                    logger.info(f"Produto deletado: {product_id}")
                else:
                    logger.warning(f"Produto não encontrado para deleção: {product_id}")
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao deletar produto {product_id}: {str(e)}", exc_info=True)
            raise ApplicationException(
                message=f"Erro BD ao deletar produto {product_id}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao deletar produto {product_id}: {str(e)}", exc_info=True)
            raise ApplicationException(
                message=f"Erro interno ao deletar produto {product_id}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_bulk_by_ids(self, product_ids: list[int]) -> list[ProductEntity]:
        """Retrieve multiple products by a list of IDs."""
        try:
            logger.debug(f"get_bulk_by_ids - IDs: {product_ids}")
            async with async_session() as session:
                stmt = select(ProductORM).where(ProductORM.id.in_(product_ids))
                result = await session.execute(stmt)
                rows = result.scalars().all()
                logger.info(f"Produtos recuperados em lote: {len(rows)}")
                return [self.converter.orm_to_entity(orm) for orm in rows]
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao recuperar produtos em lote: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao recuperar produtos em lote",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao recuperar produtos em lote: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao recuperar produtos em lote",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
