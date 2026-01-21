from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.services.product_service import ProductService
from app.core.dependencies import get_product_service
from app.core.exceptions import ApplicationException
from app.presentation.schemas.product_schema import (
    CreateProductInput,
    ProductOutput,
    UpdateProductInput,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "",
    response_model=ProductOutput,
    status_code=201,
    summary="Criar novo produto",
    description="Cria um novo produto no banco de dados",
)
async def create_product(
    request: CreateProductInput,
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
        return await service.create_product(dto)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "",
    response_model=list[ProductOutput],
    summary="Listar produtos",
    description="Recupera uma lista de produtos com paginação",
)
async def get_all_products(
    skip: int = Query(0, ge=0, description="Número de itens a pular"),
    limit: int = Query(10, ge=1, le=100, description="Limite de itens a retornar"),
    service: ProductService = Depends(get_product_service),
):
    """
    Recupera uma lista de produtos com paginação

    - **skip**: Número de itens a pular (padrão: 0)
    - **limit**: Limite de itens a retornar (padrão: 10, máximo: 100)
    """
    try:
        return await service.get_all_products(skip=skip, limit=limit)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/{product_id}",
    response_model=ProductOutput,
    summary="Obter produto por ID",
    description="Recupera um produto específico pelo seu ID",
)
async def get_product_by_id(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
):
    """
    Recupera um produto específico pelo seu ID

    - **product_id**: ID do produto
    """
    try:
        return await service.get_product_by_id(product_id)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch(
    "/{product_id}",
    response_model=ProductOutput,
    summary="Atualizar produto",
    description="Atualiza os detalhes de um produto existente",
)
async def patch_product_by_id(
    product_id: UUID,
    body: UpdateProductInput,
    service: ProductService = Depends(get_product_service),
):
    """
    Atualiza os detalhes de um produto existente
    """
    try:
        return await service.patch_product_by_id(product_id, body)
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
    "/{product_id}",
    status_code=200,
    summary="Deletar produto",
    description="Deleta um produto existente pelo seu ID",
)
async def delete_product_by_id(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
):
    """
    Deleta um produto existente pelo seu ID

    - **product_id**: ID do produto
    """
    try:
        await service.delete_product_by_id(product_id)
        return {"detail": "Produto deletado com sucesso"}
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
