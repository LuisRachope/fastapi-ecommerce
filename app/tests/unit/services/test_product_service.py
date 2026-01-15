import pytest
from unittest.mock import AsyncMock
from decimal import Decimal
from datetime import datetime

from app.application.services.product_service import ProductService
from app.application.dtos.product_dto import ProductResponseDTO
from app.core.exceptions import ApplicationException
from fastapi import status


class TestProductServiceGetAllProducts:
    @pytest.mark.asyncio
    async def test_get_all_products_returns_response_dtos(
        self, product_entity_list
    ):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_all.return_value = product_entity_list
        
        service = ProductService(product_repository=mock_repository)

        # Act
        result = await service.get_all_products()

        # Assert
        assert len(result) == 3
        assert all(isinstance(item, ProductResponseDTO) for item in result)
        assert result[0].name == product_entity_list[0].name
        assert result[1].name == product_entity_list[1].name
        assert result[2].name == product_entity_list[2].name
        mock_repository.get_all.assert_called_once_with(skip=0, limit=10)

    @pytest.mark.asyncio
    async def test_get_all_products_with_custom_pagination(
        self, product_entity_list
    ):
        # Arrange
        mock_repository = AsyncMock()
        filtered_products = [product_entity_list[0]]
        mock_repository.get_all.return_value = filtered_products
        
        service = ProductService(product_repository=mock_repository)

        # Act
        result = await service.get_all_products(skip=5, limit=20)

        # Assert
        assert len(result) == 1
        assert isinstance(result[0], ProductResponseDTO)
        mock_repository.get_all.assert_called_once_with(skip=5, limit=20)

    @pytest.mark.asyncio
    async def test_get_all_products_returns_empty_list_when_no_products(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_all.return_value = []
        
        service = ProductService(product_repository=mock_repository)

        # Act
        result = await service.get_all_products()

        # Assert
        assert result == []
        assert isinstance(result, list)
        mock_repository.get_all.assert_called_once_with(skip=0, limit=10)

    @pytest.mark.asyncio
    async def test_get_all_products_converts_entities_to_dtos(
        self, product_entity
    ):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_all.return_value = [product_entity]
        
        service = ProductService(product_repository=mock_repository)

        # Act
        result = await service.get_all_products()

        # Assert
        assert len(result) == 1
        dto = result[0]
        assert dto.id == product_entity.id
        assert dto.name == product_entity.name
        assert dto.description == product_entity.description
        assert dto.price == product_entity.price
        assert dto.quantity == product_entity.quantity
        assert dto.created_at == product_entity.created_at
        assert dto.updated_at == product_entity.updated_at

    @pytest.mark.asyncio
    async def test_get_all_products_propagates_application_exception(self):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_all.side_effect = ApplicationException(
            message="Database error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        service = ProductService(product_repository=mock_repository)

        # Act & Assert
        with pytest.raises(ApplicationException) as exc_info:
            await service.get_all_products()
        
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc_info.value.message == "Database error"

    @pytest.mark.asyncio
    async def test_get_all_products_uses_default_pagination_values(
        self, product_entity_list
    ):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_all.return_value = product_entity_list
        
        service = ProductService(product_repository=mock_repository)

        # Act
        result = await service.get_all_products()

        # Assert
        assert len(result) == 3
        # Verify the repository was called with default values
        mock_repository.get_all.assert_called_once_with(skip=0, limit=10)

    @pytest.mark.asyncio
    async def test_get_all_products_maintains_product_price_as_decimal(
        self, product_entity_list
    ):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_all.return_value = product_entity_list
        
        service = ProductService(product_repository=mock_repository)

        # Act
        result = await service.get_all_products()

        # Assert
        for dto in result:
            assert isinstance(dto.price, Decimal)
            assert dto.price > 0

    @pytest.mark.asyncio
    async def test_get_all_products_maintains_datetime_fields(
        self, product_entity
    ):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_all.return_value = [product_entity]
        
        service = ProductService(product_repository=mock_repository)

        # Act
        result = await service.get_all_products()

        # Assert
        assert len(result) == 1
        dto = result[0]
        assert isinstance(dto.created_at, datetime)
        assert isinstance(dto.updated_at, datetime)
        assert dto.created_at == product_entity.created_at
        assert dto.updated_at == product_entity.updated_at

    @pytest.mark.asyncio
    async def test_get_all_products_repository_called_once(
        self, product_entity_list
    ):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_all.return_value = product_entity_list
        
        service = ProductService(product_repository=mock_repository)

        # Act
        await service.get_all_products(skip=10, limit=5)

        # Assert
        mock_repository.get_all.assert_called_once_with(skip=10, limit=5)

    @pytest.mark.asyncio
    async def test_get_all_products_multiple_calls_independent(
        self, product_entity_list
    ):
        # Arrange
        mock_repository = AsyncMock()
        mock_repository.get_all.side_effect = [
            product_entity_list,  # First call
            [product_entity_list[0]],  # Second call
            []  # Third call
        ]
        
        service = ProductService(product_repository=mock_repository)

        # Act
        result1 = await service.get_all_products(skip=0, limit=10)
        result2 = await service.get_all_products(skip=10, limit=10)
        result3 = await service.get_all_products(skip=20, limit=10)

        # Assert
        assert len(result1) == 3
        assert len(result2) == 1
        assert len(result3) == 0
        assert mock_repository.get_all.call_count == 3
