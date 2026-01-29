from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import ApplicationException
from app.domain.entities.order_item_entity import OrderItemEntity
from app.infrastructure.persistence.repositories.order_item_repository_impl import (
    SQLOrderItemRepository,
)


@pytest.fixture
def order_item_entity():
    return OrderItemEntity(
        id=1,
        order_id=1,
        product_id=1,
        quantity=2,
        price=Decimal("50.00"),
    )


@pytest.fixture
def order_item_entity_list():
    return [
        OrderItemEntity(
            id=i + 1,
            order_id=1,
            product_id=i + 1,
            quantity=2,
            price=Decimal("50.00"),
        )
        for i in range(3)
    ]


@pytest.fixture
def mock_converter():
    return MagicMock()


class TestOrderItemRepositoryCreate:
    @pytest.mark.asyncio
    async def test_create_returns_order_item_successfully(self, mock_converter, order_item_entity):
        mock_session = AsyncMock()
        mock_orm = MagicMock()
        mock_converter.entity_to_orm.return_value = mock_orm
        mock_converter.orm_to_entity.return_value = order_item_entity

        with patch(
            "app.infrastructure.persistence.repositories.order_item_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderItemRepository()
            repository.converter = mock_converter

            result = await repository.create(order_item_entity)

            assert result == order_item_entity
            mock_session.add.assert_called_once_with(mock_orm)
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_orm)

    @pytest.mark.asyncio
    async def test_create_handles_sqlalchemy_error(self, mock_converter, order_item_entity):
        mock_session = AsyncMock()
        mock_session.commit = AsyncMock(side_effect=SQLAlchemyError("DB Error", None, None))

        with patch(
            "app.infrastructure.persistence.repositories.order_item_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderItemRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.create(order_item_entity)

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro BD ao criar item de pedido" in exc.value.message

    @pytest.mark.asyncio
    async def test_create_handles_generic_exception(self, mock_converter, order_item_entity):
        mock_session = AsyncMock()
        mock_session.commit = AsyncMock(side_effect=Exception("Unexpected error"))

        with patch(
            "app.infrastructure.persistence.repositories.order_item_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderItemRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.create(order_item_entity)

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro interno ao criar item de pedido" in exc.value.message


class TestOrderItemRepositoryCreateBulk:
    @pytest.mark.asyncio
    async def test_create_bulk_returns_order_items_successfully(
        self, mock_converter, order_item_entity_list
    ):
        mock_session = AsyncMock()
        mock_orms = [MagicMock() for _ in order_item_entity_list]
        mock_converter.entity_to_orm.side_effect = mock_orms
        mock_converter.orm_to_entity.side_effect = order_item_entity_list

        with patch(
            "app.infrastructure.persistence.repositories.order_item_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderItemRepository()
            repository.converter = mock_converter

            result = await repository.create_bulk(order_item_entity_list)

            assert len(result) == 3
            assert result == order_item_entity_list
            mock_session.add_all.assert_called_once_with(mock_orms)
            mock_session.commit.assert_called_once()
            assert mock_session.refresh.call_count == 3

    @pytest.mark.asyncio
    async def test_create_bulk_with_single_item(self, mock_converter, order_item_entity):
        mock_session = AsyncMock()
        mock_orm = MagicMock()
        mock_converter.entity_to_orm.return_value = mock_orm
        mock_converter.orm_to_entity.return_value = order_item_entity

        with patch(
            "app.infrastructure.persistence.repositories.order_item_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderItemRepository()
            repository.converter = mock_converter

            result = await repository.create_bulk([order_item_entity])

            assert len(result) == 1
            assert result[0] == order_item_entity

    @pytest.mark.asyncio
    async def test_create_bulk_with_empty_list(self, mock_converter):
        mock_session = AsyncMock()

        with patch(
            "app.infrastructure.persistence.repositories.order_item_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderItemRepository()
            repository.converter = mock_converter

            result = await repository.create_bulk([])

            assert result == []
            mock_session.add_all.assert_called_once_with([])
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_bulk_handles_sqlalchemy_error(
        self, mock_converter, order_item_entity_list
    ):
        mock_session = AsyncMock()
        mock_session.commit = AsyncMock(side_effect=SQLAlchemyError("DB Error", None, None))

        with patch(
            "app.infrastructure.persistence.repositories.order_item_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderItemRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.create_bulk(order_item_entity_list)

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro BD ao criar itens de pedido em lote" in exc.value.message

    @pytest.mark.asyncio
    async def test_create_bulk_handles_generic_exception(
        self, mock_converter, order_item_entity_list
    ):
        mock_session = AsyncMock()
        mock_session.commit = AsyncMock(side_effect=Exception("Unexpected error"))

        with patch(
            "app.infrastructure.persistence.repositories.order_item_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderItemRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.create_bulk(order_item_entity_list)

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro interno ao criar itens de pedido em lote" in exc.value.message

    @pytest.mark.asyncio
    async def test_create_bulk_with_large_quantity(self, mock_converter):
        items = [
            OrderItemEntity(
                id=i + 1,
                order_id=1,
                product_id=i + 1,
                quantity=100,
                price=Decimal("10.00"),
            )
            for i in range(10)
        ]

        mock_session = AsyncMock()
        mock_orms = [MagicMock() for _ in items]
        mock_converter.entity_to_orm.side_effect = mock_orms
        mock_converter.orm_to_entity.side_effect = items

        with patch(
            "app.infrastructure.persistence.repositories.order_item_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderItemRepository()
            repository.converter = mock_converter

            result = await repository.create_bulk(items)

            assert len(result) == 10
            mock_session.add_all.assert_called_once()
            assert mock_session.refresh.call_count == 10

    @pytest.mark.asyncio
    async def test_create_bulk_preserves_order(self, mock_converter):
        items = [
            OrderItemEntity(id=3, order_id=1, product_id=3, quantity=5, price=Decimal("30.00")),
            OrderItemEntity(id=1, order_id=1, product_id=1, quantity=2, price=Decimal("10.00")),
            OrderItemEntity(id=2, order_id=1, product_id=2, quantity=3, price=Decimal("20.00")),
        ]

        mock_session = AsyncMock()
        mock_orms = [MagicMock() for _ in items]
        mock_converter.entity_to_orm.side_effect = mock_orms
        mock_converter.orm_to_entity.side_effect = items

        with patch(
            "app.infrastructure.persistence.repositories.order_item_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderItemRepository()
            repository.converter = mock_converter

            result = await repository.create_bulk(items)

            assert result[0].id == 3
            assert result[1].id == 1
            assert result[2].id == 2
