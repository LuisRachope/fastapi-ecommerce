from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.dtos.order_dto import OrderDTO, OrderResponseDTO
from app.application.dtos.order_item_dto import OrderItemDTO
from app.application.services.order_service import OrderService
from app.domain.entities.order_entity import OrderCompleteEntity
from app.domain.entities.order_item_entity import OrderItemEntity
from app.domain.repositories.order_item_repository import OrderItemRepository
from app.domain.repositories.order_repository import OrderRepository


@pytest.fixture
def order_entity() -> OrderCompleteEntity:
    """Fixture para uma amostra de OrderCompleteEntity."""
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
        status="Pending",
        total_amount=250.00,
        items=items,
    )


@pytest.fixture
def order_entity_list() -> list[OrderCompleteEntity]:
    """Fixture para uma lista de OrderCompleteEntity."""
    return [
        OrderCompleteEntity(
            id=i + 1,
            order_date=datetime.now(),
            status="Pending",
            total_amount=Decimal("100.00"),
            items=[],
        )
        for i in range(3)
    ]


@pytest.fixture
def mock_order_repository():
    """Fixture para OrderRepository mockado."""
    return MagicMock(spec=OrderRepository)


@pytest.fixture
def mock_order_item_repository():
    """Fixture para OrderItemRepository mockado."""
    return MagicMock(spec=OrderItemRepository)


@pytest.fixture
def order_service(mock_order_repository, mock_order_item_repository):
    """Fixture para OrderService com repositório mockado."""
    return OrderService(
        order_repository=mock_order_repository, order_item_repository=mock_order_item_repository
    )


class TestOrderService:
    """Testes para OrderService."""

    @pytest.mark.asyncio
    async def test_get_all_orders_returns_list_of_dtos(
        self, order_service: OrderService, mock_order_repository: OrderRepository, order_entity_list
    ):
        """Testa que get_all_orders retorna lista de OrderResponseDTO."""
        # Arrange
        mock_order_repository.get_all = AsyncMock(return_value=order_entity_list)

        # Act
        response = await order_service.get_all_orders()

        # Assert
        assert len(response) == 3
        assert all(isinstance(item, OrderResponseDTO) for item in response)
        assert response[0].id == order_entity_list[0].id
        assert response[1].id == order_entity_list[1].id
        assert response[2].id == order_entity_list[2].id
        mock_order_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_orders_returns_empty_list(
        self, order_service: OrderService, mock_order_repository: OrderRepository
    ):
        """Testa que get_all_orders retorna lista vazia quando não há pedidos."""
        # Arrange
        mock_order_repository.get_all = AsyncMock(return_value=[])

        # Act
        response = await order_service.get_all_orders()

        # Assert
        assert response == []
        mock_order_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_order_success(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
        mock_order_item_repository: OrderItemRepository,
        order_entity: OrderCompleteEntity,
    ):
        """Testa que create_order cria um pedido com sucesso."""
        order_data = OrderDTO(
            order_date=datetime.now(),
            status="Pending",
            total_amount=Decimal("100.00"),
            items=[
                OrderItemDTO(
                    product_id=1,
                    quantity=2,
                    price=Decimal("50.00"),
                )
            ],
        )

        mock_order_repository.create = AsyncMock(return_value=order_entity)
        mock_order_item_repository.create = AsyncMock(return_value=order_entity.items[0])

        # Act
        response = await order_service.create_order(order_data)

        # Assert
        assert response.id == order_entity.id
        assert response.total_amount == order_entity.total_amount
        assert len(response.items) == len(order_entity.items)
        mock_order_repository.create.assert_called_once()
        mock_order_item_repository.create.assert_called()
