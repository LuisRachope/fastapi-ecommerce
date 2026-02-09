from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.application.services.auth_service import AuthService
from app.application.services.order_item_service import OrderItemService
from app.application.services.order_service import OrderService
from app.application.services.product_service import ProductService
from app.core.security import decode_access_token
from app.infrastructure.persistence.repositories.order_item_repository_impl import (
    SQLOrderItemRepository,
)
from app.infrastructure.persistence.repositories.order_repository_impl import SQLOrderRepository
from app.infrastructure.persistence.repositories.product_repository_impl import SQLProductRepository
from app.infrastructure.persistence.repositories.user_repository_impl import SQLUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class DependencyContainer:
    def __init__(self):
        self._repositories = {}
        self._services = {}
        self._initialize_repositories()
        self._initialize_services()

    def _initialize_repositories(self):
        """Initialize all repositories as singletons"""
        self._repositories["product_repository"] = SQLProductRepository()
        self._repositories["order_repository"] = SQLOrderRepository()
        self._repositories["order_item_repository"] = SQLOrderItemRepository()
        self._repositories["user_repository"] = SQLUserRepository()

    def _initialize_services(self):
        """Initialize all services with repository dependencies"""
        self._services["product_service"] = ProductService(
            product_repository=self._repositories["product_repository"]
        )

        self._services["order_service"] = OrderService(
            order_repository=self._repositories["order_repository"],
            order_item_repository=self._repositories["order_item_repository"],
            product_repository=self._repositories["product_repository"],
        )

        self._services["order_item_service"] = OrderItemService(
            order_item_repository=self._repositories["order_item_repository"],
        )

        self._services["auth_service"] = AuthService(
            user_repository=self._repositories["user_repository"],
        )

    # Service getters
    def get_product_service(self) -> ProductService:
        return self._services["product_service"]

    def get_order_service(self) -> OrderService:
        return self._services["order_service"]

    def get_order_item_service(self) -> OrderItemService:
        return self._services["order_item_service"]

    def get_auth_service(self) -> AuthService:
        return self._services["auth_service"]


# Global container instance
dependency_container = DependencyContainer()


# FastAPI dependency functions
def get_product_service() -> ProductService:
    return dependency_container.get_product_service()


def get_order_service() -> OrderService:
    return dependency_container.get_order_service()


def get_order_item_service() -> OrderItemService:
    return dependency_container.get_order_item_service()


def get_auth_service() -> AuthService:
    return dependency_container.get_auth_service()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Dependency que valida o token JWT e retorna o usuário atual.
    Usar em endpoints que requerem autenticação.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    try:
        user = await auth_service.get_current_user(email)
        return user
    except Exception:
        raise credentials_exception


async def get_current_active_superuser(
    current_user=Depends(get_current_user),
):
    """
    Dependency que verifica se o usuário atual é superusuário.
    Usar em endpoints administrativos.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente",
        )
    return current_user
