from datetime import datetime


class CreateUserDTO:
    """DTO para criação de usuário"""

    def __init__(
        self,
        email: str,
        password: str,
        full_name: str,
    ):
        self.email = email
        self.password = password
        self.full_name = full_name


class UserResponseDTO:
    """DTO de resposta do usuário"""

    def __init__(
        self,
        id: int,
        email: str,
        full_name: str,
        is_active: bool,
        is_superuser: bool,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.email = email
        self.full_name = full_name
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class LoginDTO:
    """DTO para login"""

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


class TokenDTO:
    """DTO de token de acesso"""

    def __init__(
        self,
        access_token: str,
        token_type: str = "bearer",
    ):
        self.access_token = access_token
        self.token_type = token_type
