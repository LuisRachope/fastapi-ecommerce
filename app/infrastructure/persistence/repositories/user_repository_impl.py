import logging

from fastapi import status
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.databases.database import async_session
from app.core.exceptions import ApplicationException
from app.domain.entities.user_entity import UserEntity
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.converters import UserConverter
from app.infrastructure.persistence.models.user_orm_model import UserORM

logger = logging.getLogger(__name__)


class SQLUserRepository(UserRepository):
    """Implementação SQLAlchemy do repositório de usuários"""

    def __init__(self):
        self.converter = UserConverter()

    async def create(self, user: UserEntity) -> UserEntity:
        """Cria um novo usuário no banco de dados"""
        try:
            logger.info(f"Criando usuário: {user.email}")
            async with async_session() as session:
                orm_obj = self.converter.entity_to_orm(user)
                session.add(orm_obj)
                await session.commit()
                await session.refresh(orm_obj)
                result = self.converter.orm_to_entity(orm_obj)
                logger.info(f"Usuário criado. ID: {result.id}")
                return result
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao criar usuário: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao criar usuário",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao criar usuário: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao criar usuário",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        """Busca usuário por ID"""
        try:
            logger.debug(f"Buscando usuário: {user_id}")
            async with async_session() as session:
                query = select(UserORM).where(UserORM.id == user_id)
                result = await session.execute(query)
                orm_obj = result.scalar_one_or_none()
                if orm_obj:
                    logger.info(f"Usuário encontrado: {user_id}")
                    return self.converter.orm_to_entity(orm_obj)
                logger.info(f"Usuário não encontrado: {user_id}")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao buscar usuário: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao buscar usuário",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao buscar usuário: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao buscar usuário",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_by_email(self, email: str) -> UserEntity | None:
        """Busca usuário por email"""
        try:
            logger.debug(f"Buscando usuário por email: {email}")
            async with async_session() as session:
                query = select(UserORM).where(UserORM.email == email)
                result = await session.execute(query)
                orm_obj = result.scalar_one_or_none()
                if orm_obj:
                    logger.info(f"Usuário encontrado: {email}")
                    return self.converter.orm_to_entity(orm_obj)
                logger.info(f"Usuário não encontrado: {email}")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao buscar usuário por email: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao buscar usuário",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao buscar usuário por email: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao buscar usuário",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[UserEntity]:
        """Lista todos os usuários com paginação"""
        try:
            logger.debug(f"get_all - skip: {skip}, limit: {limit}")
            async with async_session() as session:
                stmt = select(UserORM).offset(skip).limit(limit)
                result = await session.execute(stmt)
                rows = result.scalars().all()
                logger.info(f"Usuários recuperados: {len(rows)}")
                return [self.converter.orm_to_entity(orm) for orm in rows]
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao recuperar usuários: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao recuperar usuários",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao recuperar usuários: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao recuperar usuários",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def update(self, user: UserEntity) -> UserEntity:
        """Atualiza um usuário existente"""
        try:
            logger.info(f"Atualizando usuário: {user.id}")
            async with async_session() as session:
                query = select(UserORM).where(UserORM.id == user.id)
                result = await session.execute(query)
                orm_obj = result.scalar_one_or_none()

                if not orm_obj:
                    raise ApplicationException(
                        message=f"Usuário com ID {user.id} não encontrado",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )

                orm_obj.email = user.email
                orm_obj.full_name = user.full_name
                orm_obj.hashed_password = user.hashed_password
                orm_obj.is_active = user.is_active
                orm_obj.is_superuser = user.is_superuser

                await session.commit()
                await session.refresh(orm_obj)
                logger.info(f"Usuário atualizado: {user.id}")
                return self.converter.orm_to_entity(orm_obj)
        except ApplicationException:
            raise
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao atualizar usuário: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao atualizar usuário",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao atualizar usuário: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao atualizar usuário",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def delete_by_id(self, user_id: int) -> None:
        """Remove um usuário por ID"""
        try:
            logger.info(f"Removendo usuário: {user_id}")
            async with async_session() as session:
                stmt = delete(UserORM).where(UserORM.id == user_id)
                await session.execute(stmt)
                await session.commit()
                logger.info(f"Usuário removido: {user_id}")
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao remover usuário: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao remover usuário",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao remover usuário: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao remover usuário",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def exists_by_email(self, email: str) -> bool:
        """Verifica se existe um usuário com o email informado"""
        try:
            logger.debug(f"Verificando existência de email: {email}")
            async with async_session() as session:
                query = select(UserORM.id).where(UserORM.email == email)
                result = await session.execute(query)
                exists = result.scalar_one_or_none() is not None
                logger.debug(f"Email existe: {exists}")
                return exists
        except SQLAlchemyError as e:
            logger.error(f"Erro BD ao verificar email: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro BD ao verificar email",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Erro interno ao verificar email: {str(e)}", exc_info=True)
            raise ApplicationException(
                message="Erro interno ao verificar email",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
