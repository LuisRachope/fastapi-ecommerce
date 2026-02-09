import logging
from datetime import timedelta

from app.application.dtos.user_dto import CreateUserDTO, LoginDTO, TokenDTO, UserResponseDTO
from app.core.config import settings
from app.core.exceptions import AuthenticationException, ValidationException
from app.core.security import create_access_token, get_password_hash, verify_password
from app.domain.entities.user_entity import UserEntity
from app.domain.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class AuthService:
    """Serviço de autenticação"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, dto: CreateUserDTO) -> UserResponseDTO:
        """Registra um novo usuário"""
        self._validate_registration_data(dto)

        if await self.user_repository.exists_by_email(dto.email):
            raise ValidationException("Email já está em uso")

        hashed_password = get_password_hash(dto.password)

        user = UserEntity(
            email=dto.email,
            hashed_password=hashed_password,
            full_name=dto.full_name,
        )

        created_user = await self.user_repository.create(user)
        logger.info(f"Usuário registrado: {created_user.email}")

        return self._to_response_dto(created_user)

    async def authenticate_user(self, dto: LoginDTO) -> TokenDTO:
        """Autentica um usuário e retorna o token de acesso"""
        user = await self.user_repository.get_by_email(dto.email)

        if not user:
            logger.warning(f"Tentativa de login com email inexistente: {dto.email}")
            raise AuthenticationException("Credenciais inválidas")

        if not verify_password(dto.password, user.hashed_password):
            logger.warning(f"Senha incorreta para usuário: {dto.email}")
            raise AuthenticationException("Credenciais inválidas")

        if not user.is_active:
            logger.warning(f"Tentativa de login com usuário inativo: {dto.email}")
            raise AuthenticationException("Usuário inativo")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires,
        )

        logger.info(f"Login realizado: {dto.email}")
        return TokenDTO(access_token=access_token)

    async def get_current_user(self, email: str) -> UserResponseDTO:
        """Retorna o usuário atual pelo email"""
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise AuthenticationException("Usuário não encontrado")

        if not user.is_active:
            raise AuthenticationException("Usuário inativo")

        return self._to_response_dto(user)

    async def get_user_by_id(self, user_id: int) -> UserResponseDTO:
        """Retorna um usuário por ID"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValidationException(f"Usuário com ID {user_id} não encontrado")

        return self._to_response_dto(user)

    async def list_users(self, skip: int = 0, limit: int = 10) -> list[UserResponseDTO]:
        """Lista todos os usuários"""
        users = await self.user_repository.get_all(skip=skip, limit=limit)
        return [self._to_response_dto(u) for u in users]

    def _validate_registration_data(self, dto: CreateUserDTO) -> None:
        """Valida dados de registro"""
        if not dto.email or len(dto.email.strip()) == 0:
            raise ValidationException("Email é obrigatório")

        if "@" not in dto.email:
            raise ValidationException("Email inválido")

        if not dto.password or len(dto.password) < 6:
            raise ValidationException("Senha deve ter pelo menos 6 caracteres")

        if not dto.full_name or len(dto.full_name.strip()) == 0:
            raise ValidationException("Nome completo é obrigatório")

    def _to_response_dto(self, user: UserEntity) -> UserResponseDTO:
        """Converte entidade para DTO de resposta"""
        return UserResponseDTO(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
