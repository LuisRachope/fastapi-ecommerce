from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.order_dto import OrderInputDTO, OrderResponseDTO
from app.application.dtos.user_dto import UserResponseDTO
from app.application.use_cases.order_use_case import OrderUseCase
from app.core.dependencies import get_current_user, get_order_use_case
from app.core.exceptions import ApplicationException

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(
    "/create",
    status_code=201,
    summary="Criar novo pedido",
    description="Cria um novo pedido no sistema",
    response_model=OrderResponseDTO,
)
async def create_order(
    body: OrderInputDTO,
    current_user: UserResponseDTO = Depends(get_current_user),
    service: OrderUseCase = Depends(get_order_use_case),
):
    """
    Cria um novo pedido
    """
    try:
        return await service.create_order(body)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "",
    response_model=list[OrderResponseDTO],
    summary="Listar pedidos",
    description="Recupera todos os pedidos",
)
async def get_all_orders(
    current_user: UserResponseDTO = Depends(get_current_user),
    service: OrderUseCase = Depends(get_order_use_case),
):
    """
    Recupera todos os pedidos
    """
    try:
        return await service.get_all_orders()
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
    "/{order_id}",
    status_code=200,
    summary="Deletar pedido",
    description="Deleta um pedido pelo ID",
    response_model=bool,
)
async def delete_order_by_id(
    order_id: str,
    current_user: UserResponseDTO = Depends(get_current_user),
    service: OrderUseCase = Depends(get_order_use_case),
):
    """
    Deleta um pedido pelo ID
    """
    try:
        return await service.delete_order_by_id(order_id)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
