import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError

from app.infrastructure.persistence.repositories.product_repository_impl import (
    SQLProductRepository,
)
from app.core.exceptions import ApplicationException
from fastapi import status


class TestProductRepositoryGetAll:
    @pytest.mark.asyncio
    async def test_get_all_returns_products_successfully(
        self, mock_converter, product_entity_list, mock_async_session_context
    ):
        # Arrange
        skip, limit = 0, 10
        repository = SQLProductRepository()
        repository.converter = mock_converter

        # Mock the ORM objects
        mock_orm_objects = [MagicMock() for _ in product_entity_list]
        
        # Mock session.execute behavior - use MagicMock for result chain
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = mock_orm_objects
        
        mock_session = mock_async_session_context.__aenter__.return_value
        mock_session.execute = AsyncMock(return_value=mock_result)
        
        # Mock converter to return ProductEntity objects
        mock_converter.orm_to_entity.side_effect = product_entity_list

        # Act
        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=mock_async_session_context,
        ):
            result = await repository.get_all(skip=skip, limit=limit)

        # Assert
        assert len(result) == 3
        assert result == product_entity_list
        assert mock_session.execute.called
        mock_converter.orm_to_entity.assert_called()

    @pytest.mark.asyncio
    async def test_get_all_with_custom_pagination(
        self, mock_converter, product_entity_list, mock_async_session_context
    ):
        # Arrange
        skip, limit = 5, 20
        repository = SQLProductRepository()
        repository.converter = mock_converter

        mock_orm_objects = [MagicMock()]
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = mock_orm_objects
        
        mock_session = mock_async_session_context.__aenter__.return_value
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_converter.orm_to_entity.side_effect = [product_entity_list[0]]

        # Act
        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=mock_async_session_context,
        ):
            result = await repository.get_all(skip=skip, limit=limit)

        # Assert
        assert len(result) == 1
        # Verify execute was called (which includes offset and limit)
        assert mock_session.execute.called

    @pytest.mark.asyncio
    async def test_get_all_returns_empty_list(
        self, mock_converter, mock_async_session_context
    ):
        # Arrange
        repository = SQLProductRepository()
        repository.converter = mock_converter

        mock_result = MagicMock()
        mock_result.scalars().all.return_value = []
        
        mock_session = mock_async_session_context.__aenter__.return_value
        mock_session.execute = AsyncMock(return_value=mock_result)

        # Act
        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=mock_async_session_context,
        ):
            result = await repository.get_all()

        # Assert
        assert result == []
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_get_all_handles_sqlalchemy_error(
        self, mock_converter, mock_async_session_context
    ):
        # Arrange
        repository = SQLProductRepository()
        repository.converter = mock_converter

        mock_session = mock_async_session_context.__aenter__.return_value
        mock_session.execute = AsyncMock(side_effect=SQLAlchemyError("DB Error", None, None))

        # Act & Assert
        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=mock_async_session_context,
        ):
            with pytest.raises(ApplicationException) as exc_info:
                await repository.get_all()
        
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Erro BD ao recuperar produtos" in exc_info.value.message

    @pytest.mark.asyncio
    async def test_get_all_handles_generic_exception(
        self, mock_converter, mock_async_session_context
    ):
        # Arrange
        repository = SQLProductRepository()
        repository.converter = mock_converter

        mock_session = mock_async_session_context.__aenter__.return_value
        mock_session.execute = AsyncMock(side_effect=Exception("Unexpected error"))

        # Act & Assert
        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=mock_async_session_context,
        ):
            with pytest.raises(ApplicationException) as exc_info:
                await repository.get_all()
        
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Erro interno ao recuperar produtos" in exc_info.value.message

    @pytest.mark.asyncio
    async def test_get_all_default_pagination_values(
        self, mock_converter, product_entity_list, mock_async_session_context
    ):
        # Arrange
        repository = SQLProductRepository()
        repository.converter = mock_converter

        mock_orm_objects = [MagicMock() for _ in product_entity_list]
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = mock_orm_objects
        
        mock_session = mock_async_session_context.__aenter__.return_value
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_converter.orm_to_entity.side_effect = product_entity_list

        # Act
        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=mock_async_session_context,
        ):
            result = await repository.get_all()

        # Assert
        assert len(result) == 3
        assert mock_session.execute.called
