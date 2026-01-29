from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import ApplicationException
from app.domain.entities.order_entity import OrderCompleteEntity, OrderEntity
from app.domain.entities.order_item_entity import OrderItemEntity
from app.domain.enums.order_status import OrderStatus
from app.infrastructure.persistence.repositories.order_repository_impl import SQLOrderRepository


@pytest.fixture
def order_entity():
    return OrderEntity(
        id=1,
        order_date=datetime.now(),
        status=OrderStatus.PENDING.value,
        total_amount=Decimal("100.00"),
    )


@pytest.fixture
def order_complete_entity():
    items = [
        OrderItemEntity(
            id=1,
            order_id=1,
            product_id=1,
            quantity=2,
            price=Decimal("50.00"),
        )
    ]
    return OrderCompleteEntity(
        id=1,
        order_date=datetime.now(),
        status=OrderStatus.PENDING.value,
        total_amount=Decimal("100.00"),
        items=items,
    )


@pytest.fixture
def order_entity_list():
    return [
        OrderCompleteEntity(
            id=i + 1,
            order_date=datetime.now(),
            status=OrderStatus.PENDING.value,
            total_amount=Decimal("100.00"),
            items=[],
        )
        for i in range(3)
    ]


@pytest.fixture
def mock_converter():
    return MagicMock()


class TestOrderRepositoryCreate:
    @pytest.mark.asyncio
    async def test_create_returns_order_successfully(self, mock_converter, order_entity):
        mock_session = AsyncMock()
        mock_orm = MagicMock()
        mock_converter.entity_to_orm.return_value = mock_orm
        mock_converter.orm_to_entity.return_value = order_entity

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            result = await repository.create(order_entity)

            assert result == order_entity
            mock_session.add.assert_called_once_with(mock_orm)
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once_with(mock_orm)

    @pytest.mark.asyncio
    async def test_create_handles_sqlalchemy_error(self, mock_converter, order_entity):
        mock_session = AsyncMock()
        mock_session.commit = AsyncMock(side_effect=SQLAlchemyError("DB Error", None, None))

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.create(order_entity)

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro BD ao criar pedido" in exc.value.message

    @pytest.mark.asyncio
    async def test_create_handles_generic_exception(self, mock_converter, order_entity):
        mock_session = AsyncMock()
        mock_session.commit = AsyncMock(side_effect=Exception("Unexpected error"))

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.create(order_entity)

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro interno ao criar pedido" in exc.value.message


class TestOrderRepositoryGetById:
    @pytest.mark.asyncio
    async def test_get_by_id_returns_order_successfully(self, mock_converter, order_entity):
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_orm = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_orm
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_converter.orm_to_entity.return_value = order_entity

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            result = await repository.get_by_id("1")

            assert result == order_entity
            mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_returns_none_when_not_found(self, mock_converter):
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            result = await repository.get_by_id("999")

            assert result is None

    @pytest.mark.asyncio
    async def test_get_by_id_handles_sqlalchemy_error(self, mock_converter):
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=SQLAlchemyError("DB Error", None, None))

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.get_by_id("1")

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro BD ao recuperar pedido" in exc.value.message

    @pytest.mark.asyncio
    async def test_get_by_id_handles_generic_exception(self, mock_converter):
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=Exception("Unexpected error"))

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.get_by_id("1")

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro interno ao recuperar pedido" in exc.value.message


class TestOrderRepositoryGetAll:
    @pytest.mark.asyncio
    async def test_get_all_returns_orders_successfully(self, mock_converter, order_entity_list):
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = [MagicMock() for _ in order_entity_list]
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_converter.orm_to_complete_entity.side_effect = order_entity_list

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            result = await repository.get_all()

            assert len(result) == 3
            assert result == order_entity_list

    @pytest.mark.asyncio
    async def test_get_all_returns_empty_list(self, mock_converter):
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars().all.return_value = []
        mock_session.execute = AsyncMock(return_value=mock_result)

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            result = await repository.get_all()

            assert result == []

    @pytest.mark.asyncio
    async def test_get_all_handles_sqlalchemy_error(self, mock_converter):
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=SQLAlchemyError("DB Error", None, None))

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.get_all()

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro BD ao recuperar pedidos" in exc.value.message

    @pytest.mark.asyncio
    async def test_get_all_handles_generic_exception(self, mock_converter):
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=Exception("Unexpected error"))

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.get_all()

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro interno ao recuperar pedidos" in exc.value.message


class TestOrderRepositoryDeleteById:
    @pytest.mark.asyncio
    async def test_delete_by_id_returns_true_successfully(self, mock_converter):
        mock_session = AsyncMock()

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            result = await repository.delete_by_id("1")

            assert result is True
            mock_session.execute.assert_called_once()
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_by_id_handles_sqlalchemy_error(self, mock_converter):
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=SQLAlchemyError("DB Error", None, None))

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.delete_by_id("1")

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro BD ao deletar pedido" in exc.value.message

    @pytest.mark.asyncio
    async def test_delete_by_id_handles_generic_exception(self, mock_converter):
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(side_effect=Exception("Unexpected error"))

        with patch(
            "app.infrastructure.persistence.repositories.order_repository_impl.async_session",
            return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_session)),
        ):
            repository = SQLOrderRepository()
            repository.converter = mock_converter

            with pytest.raises(ApplicationException) as exc:
                await repository.delete_by_id("1")

            assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Erro interno ao deletar pedido" in exc.value.message
