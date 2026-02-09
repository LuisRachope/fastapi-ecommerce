from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.application.dtos.user_dto import CreateUserDTO, LoginDTO
from app.application.services.auth_service import AuthService
from app.core.dependencies import get_auth_service, get_current_user
from app.core.exceptions import ApplicationException, AuthenticationException, ValidationException
from app.presentation.schemas.user_schema import (
    LoginInput,
    RegisterUserInput,
    TokenOutput,
    UserOutput,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post(
    "/register",
    response_model=UserOutput,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Cria uma nova conta de usuário no sistema",
)
async def register(
    request: RegisterUserInput,
    service: AuthService = Depends(get_auth_service),
):
    """
    Registra um novo usuário no sistema

    - **email**: Email único do usuário
    - **password**: Senha com pelo menos 6 caracteres
    - **full_name**: Nome completo do usuário
    """
    try:
        dto = CreateUserDTO(
            email=request.email,
            password=request.password,
            full_name=request.full_name,
        )
        return await service.register_user(dto)
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/login",
    response_model=TokenOutput,
    summary="Fazer login",
    description="Autentica o usuário e retorna um token de acesso JWT",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    """
    Autentica o usuário com email e senha

    - **username**: Email do usuário (usando username por compatibilidade OAuth2)
    - **password**: Senha do usuário

    Retorna um token JWT para uso nas próximas requisições
    """
    try:
        dto = LoginDTO(email=form_data.username, password=form_data.password)
        token = await service.authenticate_user(dto)
        return TokenOutput(access_token=token.access_token, token_type=token.token_type)
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/login/json",
    response_model=TokenOutput,
    summary="Fazer login (JSON)",
    description="Autentica o usuário via JSON e retorna um token de acesso JWT",
)
async def login_json(
    request: LoginInput,
    service: AuthService = Depends(get_auth_service),
):
    """
    Autentica o usuário com email e senha via JSON

    - **email**: Email do usuário
    - **password**: Senha do usuário

    Retorna um token JWT para uso nas próximas requisições
    """
    try:
        dto = LoginDTO(email=request.email, password=request.password)
        token = await service.authenticate_user(dto)
        return TokenOutput(access_token=token.access_token, token_type=token.token_type)
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/me",
    response_model=UserOutput,
    summary="Obter usuário atual",
    description="Retorna as informações do usuário autenticado",
)
async def get_me(
    current_user: UserOutput = Depends(get_current_user),
):
    """
    Retorna as informações do usuário autenticado

    Requer autenticação via Bearer Token
    """
    return current_user


@router.get(
    "/users",
    response_model=list[UserOutput],
    summary="Listar usuários",
    description="Lista todos os usuários cadastrados (requer autenticação)",
)
async def list_users(
    skip: int = Query(0, ge=0, description="Número de itens a pular"),
    limit: int = Query(10, ge=1, le=100, description="Limite de itens a retornar"),
    current_user: UserOutput = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
):
    """
    Lista todos os usuários cadastrados

    - **skip**: Número de itens a pular (padrão: 0)
    - **limit**: Limite de itens a retornar (padrão: 10, máximo: 100)

    Requer autenticação via Bearer Token
    """
    try:
        return await service.list_users(skip=skip, limit=limit)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
