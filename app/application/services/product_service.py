from typing import List
from app.domain.entities.product import ProductEntity
from app.domain.repositories.product_repository import ProductRepository
from app.application.dtos.product_dto import CreateProductDTO, ProductResponseDTO
from app.core.exceptions import ApplicationException, ValidationException
from decimal import Decimal


class ProductService:
    """Serviço de aplicação para produtos"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def create_product(self, dto: CreateProductDTO) -> ProductResponseDTO:
        """
        Cria um novo produto
        Valida os dados antes de persistir
        """
        # Validações de negócio
        self._validate_product_data(dto.name, dto.price, dto.quantity)
        
        # Cria a entidade de domínio
        product = ProductEntity(
            name=dto.name,
            description=dto.description,
            price=Decimal(str(dto.price)),
            quantity=dto.quantity,
        )
        
        # Persiste no repositório
        created_product = await self.product_repository.create(product)
        
        # Retorna como DTO
        return self._to_response_dto(created_product)
    
    async def list_products(self, skip: int = 0, limit: int = 10) -> List[ProductResponseDTO]:
        """Lista todos os produtos"""
        products = await self.product_repository.get_all(skip=skip, limit=limit)
        return [self._to_response_dto(p) for p in products]
    
    def _validate_product_data(self, name: str, price: Decimal, quantity: int) -> None:
        """Valida dados do produto"""
        if not name or len(name.strip()) == 0:
            raise ValidationException("Nome do produto é obrigatório")
        
        if price <= 0:
            raise ValidationException("Preço deve ser maior que zero")
        
        if quantity < 0:
            raise ValidationException("Quantidade não pode ser negativa")
    
    def _to_response_dto(self, product: ProductEntity) -> ProductResponseDTO:
        """Converte entidade para DTO de resposta"""
        return ProductResponseDTO(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

    async def get_all_products(self, skip: int = 0, limit: int = 10) -> List[ProductResponseDTO]:
        """Recupera todos os produtos com paginação"""
        products = await self.product_repository.get_all(skip=skip, limit=limit)
        return [self._to_response_dto(p) for p in products]
    
    async def get_product_by_id(self, product_id: str) -> ProductResponseDTO:
        """Recupera um produto por ID"""
        try:
            product = await self.product_repository.get_by_id(product_id)
            if not product:
                raise ValidationException(f"Produto com ID {product_id} não encontrado")
            return self._to_response_dto(product)
        except ValidationException:
            raise
        except ApplicationException as e:
            raise ApplicationException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise ValidationException(f"Erro ao recuperar produto com ID {product_id}: {str(e)}")