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
        self, mock_converter, product_entity_list
    ):
        # Arrange
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = [MagicMock() for _ in product_entity_list]
        mock_session.execute = AsyncMock(return_value=mock_result)

        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session))
        ):
            mock_converter.orm_to_entity.side_effect = product_entity_list
            repository = SQLProductRepository()
            repository.converter = mock_converter

            # Act
            result = await repository.get_all(skip=0, limit=10)

            # Assert
            assert len(result) == 3
            assert result == product_entity_list

    @pytest.mark.asyncio
    @pytest.mark.parametrize("skip,limit", [
        (0, 10),
        (5, 20),
        (10, 5),
    ])
    async def test_get_all_with_different_pagination(
        self, mock_converter, product_entity_list, skip, limit
    ):
        # Arrange
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = [MagicMock()]
        mock_session.execute = AsyncMock(return_value=mock_result)

        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session))
        ):
            mock_converter.orm_to_entity.side_effect = [product_entity_list[0]]
            repository = SQLProductRepository()
            repository.converter = mock_converter

            # Act
            result = await repository.get_all(skip=skip, limit=limit)

            # Assert
            assert len(result) == 1

    @pytest.mark.asyncio
    async def test_get_all_returns_empty_list(
        self, mock_converter
    ):
        # Arrange
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = []
        mock_session.execute = AsyncMock(return_value=mock_result)

        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session))
        ):
            repository = SQLProductRepository()
            repository.converter = mock_converter

            # Act
            result = await repository.get_all()

            # Assert
            assert result == []

    @pytest.mark.asyncio
    async def test_get_all_handles_sqlalchemy_error(
        self, mock_converter
    ):
        # Arrange
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=SQLAlchemyError("DB Error", None, None))

        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session))
        ):
            repository = SQLProductRepository()
            repository.converter = mock_converter

            # Act & Assert
            with pytest.raises(ApplicationException) as exc:
                await repository.get_all()

        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    @pytest.mark.asyncio
    async def test_get_all_handles_generic_exception(
        self, mock_converter
    ):
        # Arrange
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=Exception("Unexpected error"))

        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session))
        ):
            repository = SQLProductRepository()
            repository.converter = mock_converter

            # Act & Assert
            with pytest.raises(ApplicationException) as exc:
                await repository.get_all()

        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    @pytest.mark.asyncio
    async def test_get_all_default_pagination_values(
        self, mock_converter, product_entity_list
    ):
        # Arrange
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = [MagicMock() for _ in product_entity_list]
        mock_session.execute = AsyncMock(return_value=mock_result)

        with patch(
            "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session))
        ):
            mock_converter.orm_to_entity.side_effect = product_entity_list
            repository = SQLProductRepository()
            repository.converter = mock_converter

            # Act
            result = await repository.get_all()

            # Assert
            assert len(result) == 3
