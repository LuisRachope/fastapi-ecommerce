from datetime import datetime


class UserEntity:
    """Entidade de domínio do usuário"""

    def __init__(
        self,
        email: str,
        hashed_password: str,
        full_name: str,
        is_active: bool = True,
        is_superuser: bool = False,
        id: int | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
