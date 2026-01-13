from fastapi import APIRouter, HTTPException, Depends, Query
from uuid import UUID
from app.application.services.product_service import ProductService
from app.presentation.schemas.product_schema import (
    CreateProductRequest,
    ProductResponse,
)
from app.presentation.api.v1.dependencies import get_product_service
from app.core.exceptions import ApplicationException

router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    "",
    response_model=ProductResponse,
    status_code=201,
    summary="Criar novo produto",
    description="Cria um novo produto no banco de dados",
)
async def create_product(
    request: CreateProductRequest,
    service: ProductService = Depends(get_product_service),
):
    """
    Cria um novo produto
    
    - **name**: Nome do produto
    - **description**: Descrição do produto
    - **price**: Preço do produto (> 0)
    - **quantity**: Quantidade em estoque
    """
    try:
        from app.application.dtos.product_dto import CreateProductDTO
        
        dto = CreateProductDTO(
            name=request.name,
            description=request.description,
            price=request.price,
            quantity=request.quantity,
        )
        result = await service.create_product(dto)
        return result.to_dict()
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "",
    response_model=list[ProductResponse],
    summary="Listar produtos",
    description="Recupera uma lista de produtos com paginação",
)
async def get_all_products(
    skip : int = Query(0, ge=0, description="Número de itens a pular"),
    limit : int = Query(10, ge=1, le=100, description="Limite de itens a retornar"),
    service: ProductService = Depends(get_product_service),
):
    """
    Recupera uma lista de produtos com paginação
    
    - **skip**: Número de itens a pular (padrão: 0)
    - **limit**: Limite de itens a retornar (padrão: 10, máximo: 100)
    """
    try:
        products = await service.get_all_products(skip=skip, limit=limit)
        return products
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))