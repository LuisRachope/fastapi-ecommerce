from abc import ABC, abstractmethod

from app.domain.entities.user_entity import UserEntity


class UserRepository(ABC):
    """Interface abstrata do repositório de usuários"""

    @abstractmethod
    async def create(self, user: UserEntity) -> UserEntity:
        """Cria um novo usuário"""

    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserEntity | None:
        """Busca usuário por ID"""

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None:
        """Busca usuário por email"""

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 10) -> list[UserEntity]:
        """Lista todos os usuários com paginação"""

    @abstractmethod
    async def update(self, user: UserEntity) -> UserEntity:
        """Atualiza um usuário existente"""

    @abstractmethod
    async def delete_by_id(self, user_id: int) -> None:
        """Remove um usuário por ID"""

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Verifica se existe um usuário com o email informado"""
