from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import status

from app.application.dtos.order_dto import OrderInputDTO, OrderResponseDTO
from app.application.dtos.order_item_dto import OrderItemInputDTO
from app.application.services.order_service import OrderService
from app.domain.entities.order_entity import OrderCompleteEntity, OrderEntity
from app.domain.entities.order_item_entity import OrderItemEntity
from app.domain.entities.product_entity import ProductEntity
from app.domain.enums.order_status import OrderStatus
from app.domain.repositories.order_item_repository import OrderItemRepository
from app.domain.repositories.order_repository import OrderRepository
from app.domain.repositories.product_repository import ProductRepository


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
        status=OrderStatus.PENDING.value,
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
            status=OrderStatus.PENDING.value,
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
def mock_product_repository():
    """Fixture para ProductRepository mockado."""
    return MagicMock(spec=ProductRepository)


@pytest.fixture
def order_service(mock_order_repository, mock_order_item_repository, mock_product_repository):
    """Fixture para OrderService com repositório mockado."""
    return OrderService(
        order_repository=mock_order_repository,
        order_item_repository=mock_order_item_repository,
        product_repository=mock_product_repository,
    )


class TestOrderService:
    """Testes para OrderService."""

    @pytest.mark.asyncio
    async def test_get_all_orders_returns_list_of_dtos(
        self, order_service: OrderService, mock_order_repository: OrderRepository, order_entity_list
    ):
        """Testa que get_all_orders retorna lista de OrderResponseDTO."""
        mock_order_repository.get_all = AsyncMock(return_value=order_entity_list)

        response = await order_service.get_all_orders()

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
        mock_order_repository.get_all = AsyncMock(return_value=[])

        response = await order_service.get_all_orders()

        assert response == []
        mock_order_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_order_success(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
        mock_order_item_repository: OrderItemRepository,
        mock_product_repository,
    ):
        """Testa que create_order cria um pedido com sucesso."""
        order_data = OrderInputDTO(
            items=[
                OrderItemInputDTO(
                    product_id=1,
                    quantity=2,
                )
            ],
        )

        product = ProductEntity(
            id=1,
            name="Product 1",
            description="Description",
            price=Decimal("50.00"),
            quantity=10,
        )

        order_entity = OrderEntity(
            id=1,
            order_date=datetime.now(),
            status=OrderStatus.PENDING.value,
            total_amount=Decimal("100.00"),
        )

        item_entities = [
            OrderItemEntity(
                id=1,
                order_id=1,
                product_id=1,
                quantity=2,
                price=Decimal("50.00"),
            )
        ]

        mock_product_repository.get_bulk_by_ids = AsyncMock(return_value=[product])
        mock_order_repository.create = AsyncMock(return_value=order_entity)
        mock_order_item_repository.create_bulk = AsyncMock(return_value=item_entities)

        response = await order_service.create_order(order_data)

        assert response.id == order_entity.id
        assert len(response.items) == 1
        mock_order_repository.create.assert_called_once()
        mock_order_item_repository.create_bulk.assert_called_once()
        mock_product_repository.get_bulk_by_ids.assert_called_once_with([1])

    @pytest.mark.asyncio
    async def test_create_order_with_empty_items_returns_422(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
    ):
        """Testa que create_order retorna erro 422 quando a lista de itens está vazia."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            order_data = OrderInputDTO(
                items=[],
            )

        assert "A lista de itens não pode estar vazia" in str(exc_info.value)
        mock_order_repository.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_order_handles_application_exception(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
    ):
        """Testa que create_order propaga ApplicationException corretamente."""
        from app.core.exceptions import ApplicationException

        order_data = OrderInputDTO(
            items=[
                OrderItemInputDTO(
                    product_id=1,
                    quantity=2,
                )
            ],
        )
        mock_order_repository.create = AsyncMock(
            side_effect=ApplicationException(
                message="Erro no repositório",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        )

        with pytest.raises(ApplicationException) as exc_info:
            await order_service.create_order(order_data)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Erro no repositório" in str(exc_info.value.message)

    @pytest.mark.asyncio
    async def test_create_order_handles_generic_exception(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
    ):
        """Testa que create_order trata exceções genéricas corretamente."""
        from app.core.exceptions import ApplicationException

        order_data = OrderInputDTO(
            items=[
                OrderItemInputDTO(
                    product_id=1,
                    quantity=2,
                )
            ],
        )
        mock_order_repository.create = AsyncMock(side_effect=Exception("Erro inesperado"))

        with pytest.raises(ApplicationException) as exc_info:
            await order_service.create_order(order_data)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Erro inesperado" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_all_orders_handles_application_exception(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
    ):
        """Testa que get_all_orders propaga ApplicationException corretamente."""
        from app.core.exceptions import ApplicationException

        mock_order_repository.get_all = AsyncMock(
            side_effect=ApplicationException(
                message="Erro ao buscar pedidos",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        )

        with pytest.raises(ApplicationException) as exc_info:
            await order_service.get_all_orders()

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Erro ao buscar pedidos" in str(exc_info.value.message)

    @pytest.mark.asyncio
    async def test_get_all_orders_handles_generic_exception(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
    ):
        """Testa que get_all_orders trata exceções genéricas corretamente."""
        from app.core.exceptions import ApplicationException

        mock_order_repository.get_all = AsyncMock(side_effect=Exception("Erro no banco de dados"))

        with pytest.raises(ApplicationException) as exc_info:
            await order_service.get_all_orders()

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Erro no banco de dados" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_delete_order_by_id_success(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
        order_entity: OrderCompleteEntity,
    ):
        """Testa que delete_order_by_id deleta um pedido com sucesso."""
        order_id = "1"
        mock_order_repository.get_by_id = AsyncMock(return_value=order_entity)
        mock_order_repository.delete_by_id = AsyncMock(return_value=None)

        result = await order_service.delete_order_by_id(order_id)

        assert result is True
        mock_order_repository.get_by_id.assert_called_once_with(order_id)
        mock_order_repository.delete_by_id.assert_called_once_with(order_id)

    @pytest.mark.asyncio
    async def test_delete_order_by_id_not_found_returns_true(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
    ):
        """Testa que delete_order_by_id retorna True quando o pedido não é encontrado."""
        order_id = "999"
        mock_order_repository.get_by_id = AsyncMock(return_value=None)

        result = await order_service.delete_order_by_id(order_id)

        assert result is True
        mock_order_repository.get_by_id.assert_called_once_with(order_id)
        mock_order_repository.delete_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_order_by_id_handles_application_exception(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
    ):
        """Testa que delete_order_by_id propaga ApplicationException corretamente."""
        from app.core.exceptions import ApplicationException

        order_id = "1"
        mock_order_repository.get_by_id = AsyncMock(
            side_effect=ApplicationException(
                message="Erro ao buscar pedido",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        )

        with pytest.raises(ApplicationException) as exc_info:
            await order_service.delete_order_by_id(order_id)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Erro ao buscar pedido" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_delete_order_by_id_handles_generic_exception(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
    ):
        """Testa que delete_order_by_id trata exceções genéricas corretamente."""
        from app.core.exceptions import ApplicationException

        order_id = "1"
        mock_order_repository.get_by_id = AsyncMock(side_effect=Exception("Erro inesperado"))

        with pytest.raises(ApplicationException) as exc_info:
            await order_service.delete_order_by_id(order_id)

        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Erro inesperado" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_order_with_multiple_items_success(
        self,
        order_service: OrderService,
        mock_order_repository: OrderRepository,
        mock_order_item_repository: OrderItemRepository,
        mock_product_repository,
    ):
        """Testa que create_order cria um pedido com múltiplos itens com sucesso."""
        order_data = OrderInputDTO(
            items=[
                OrderItemInputDTO(product_id=1, quantity=2),
                OrderItemInputDTO(product_id=2, quantity=1),
                OrderItemInputDTO(product_id=3, quantity=5),
            ],
        )

        products = [
            ProductEntity(
                id=1, name="Product 1", description="Desc 1", price=Decimal("50.00"), quantity=10
            ),
            ProductEntity(
                id=2, name="Product 2", description="Desc 2", price=Decimal("100.00"), quantity=10
            ),
            ProductEntity(
                id=3, name="Product 3", description="Desc 3", price=Decimal("30.00"), quantity=10
            ),
        ]

        order_entity = OrderEntity(
            id=1,
            order_date=datetime.now(),
            status=OrderStatus.PENDING.value,
            total_amount=Decimal("350.00"),
        )

        item_entities = [
            OrderItemEntity(id=1, order_id=1, product_id=1, quantity=2, price=Decimal("50.00")),
            OrderItemEntity(id=2, order_id=1, product_id=2, quantity=1, price=Decimal("100.00")),
            OrderItemEntity(id=3, order_id=1, product_id=3, quantity=5, price=Decimal("30.00")),
        ]

        mock_product_repository.get_bulk_by_ids = AsyncMock(return_value=products)
        mock_order_repository.create = AsyncMock(return_value=order_entity)
        mock_order_item_repository.create_bulk = AsyncMock(return_value=item_entities)

        response = await order_service.create_order(order_data)

        assert response.id == order_entity.id
        assert len(response.items) == 3
        assert response.items[0].product_id == 1
        assert response.items[1].product_id == 2
        assert response.items[2].product_id == 3
        mock_order_repository.create.assert_called_once()
        mock_order_item_repository.create_bulk.assert_called_once()
