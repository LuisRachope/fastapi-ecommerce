from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.order_dto import OrderDTO, OrderResponseDTO
from app.application.services.order_service import OrderService
from app.core.dependencies import get_order_service
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
    body: OrderDTO,
    service: OrderService = Depends(get_order_service),
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
