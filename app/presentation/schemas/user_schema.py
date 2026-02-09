from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RegisterUserInput(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=6, max_length=100, description="Senha do usuário")
    full_name: str = Field(..., min_length=2, max_length=255, description="Nome completo")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "password": "senha123",
                "full_name": "João Silva",
            }
        }


class LoginInput(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=1, description="Senha do usuário")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "password": "senha123",
            }
        }


class TokenOutput(BaseModel):
    access_token: str = Field(..., description="Token de acesso JWT")
    token_type: str = Field(default="bearer", description="Tipo do token")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }


class UserOutput(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "usuario@exemplo.com",
                "full_name": "João Silva",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2025-01-07T10:30:00",
                "updated_at": "2025-01-07T10:30:00",
            }
        }
