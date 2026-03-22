from contextvars import ContextVar

from app.application.dtos.user_dto import UserResponseDTO

_current_user: ContextVar[UserResponseDTO | None] = ContextVar("current_user", default=None)


def set_current_user(user: UserResponseDTO) -> None:
    """Define o usuário autenticado no contexto da request atual."""
    _current_user.set(user)


def get_current_user_from_context() -> UserResponseDTO:
    """
    Retorna o usuário autenticado do contexto da request atual.
    Pode ser usado em qualquer camada (services, repositories, etc.)

    Raises:
        RuntimeError: Se não houver usuário autenticado no contexto.
    """
    user = _current_user.get()
    if user is None:
        raise RuntimeError("Nenhum usuário autenticado no contexto da request")
    return user


def get_current_user_id() -> int:
    """Atalho para obter apenas o ID do usuário autenticado."""
    return get_current_user_from_context().id
