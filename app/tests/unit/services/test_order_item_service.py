from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.dtos.order_item_dto import OrderItemDTO, OrderItemResponseDTO
from app.application.services.order_item_service import OrderItemService
from app.domain.entities.order_item_entity import OrderItemEntity
from app.domain.repositories.order_item_repository import OrderItemRepository


@pytest.fixture
def order_item_entity() -> OrderItemEntity:
    """Fixture para uma amostra de OrderItemEntity."""
    return OrderItemEntity(
        id=1,
        order_id=1,
        product_id=1,
        quantity=2,
        price=Decimal("50.00"),
    )


@pytest.fixture
def order_item_dto() -> OrderItemDTO:
    """Fixture para uma amostra de OrderItemDTO."""
    return OrderItemDTO(
        product_id=1,
        quantity=2,
        price=50.00,
    )


@pytest.fixture
def order_item_response_dto() -> OrderItemResponseDTO:
    """Fixture para uma amostra de OrderItemResponseDTO."""
    return OrderItemResponseDTO(
        id=1,
        order_id=1,
        product_id=1,
        quantity=2,
        price=50.00,
    )


@pytest.fixture
def mock_order_item_repository():
    """Fixture para OrderItemRepository mockado."""
    return MagicMock(spec=OrderItemRepository)


@pytest.fixture
def order_item_service(mock_order_item_repository):
    """Fixture para OrderItemService com repositório mockado."""
    return OrderItemService(order_item_repository=mock_order_item_repository)


class TestOrderItemService:
    """Testes para OrderItemService."""

    @pytest.mark.asyncio
    async def test_create_order_item_success(
        self,
        order_item_service: OrderItemService,
        mock_order_item_repository: OrderItemRepository,
        order_item_dto: OrderItemDTO,
        order_item_response_dto: OrderItemResponseDTO,
    ):
        """Testa que create_order_item cria um item de pedido com sucesso."""
        mock_order_item_repository.create = AsyncMock(return_value=order_item_response_dto)

        response = await order_item_service.create_order_item(order_item_dto)

        assert response.id == order_item_response_dto.id
        assert response.product_id == order_item_response_dto.product_id
        assert response.order_id == order_item_response_dto.order_id
        assert response.quantity == order_item_response_dto.quantity
        assert response.price == order_item_response_dto.price
        mock_order_item_repository.create.assert_called_once_with(order_item_dto)

    @pytest.mark.asyncio
    async def test_create_order_item_with_zero_quantity_validation(
        self,
        order_item_service: OrderItemService,
    ):
        """Testa que create_order_item valida quantidade zero."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            OrderItemDTO(
                product_id=1,
                quantity=0,
                price=50.00,
            )

    @pytest.mark.asyncio
    async def test_create_order_item_with_negative_quantity_validation(
        self,
        order_item_service: OrderItemService,
    ):
        """Testa que create_order_item valida quantidade negativa."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            OrderItemDTO(
                product_id=1,
                quantity=-5,
                price=50.00,
            )

    @pytest.mark.asyncio
    async def test_create_order_item_with_zero_price_validation(
        self,
        order_item_service: OrderItemService,
    ):
        """Testa que create_order_item valida preço zero."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            OrderItemDTO(
                product_id=1,
                quantity=2,
                price=0.0,
            )

    @pytest.mark.asyncio
    async def test_create_order_item_with_negative_price_validation(
        self,
        order_item_service: OrderItemService,
    ):
        """Testa que create_order_item valida preço negativo."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            OrderItemDTO(
                product_id=1,
                quantity=2,
                price=-10.0,
            )

    @pytest.mark.asyncio
    async def test_create_order_item_with_invalid_product_id(
        self,
        order_item_service: OrderItemService,
    ):
        """Testa que create_order_item valida product_id inválido."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            OrderItemDTO(
                product_id=0,
                quantity=2,
                price=50.00,
            )

    @pytest.mark.asyncio
    async def test_create_order_item_repository_exception(
        self,
        order_item_service: OrderItemService,
        mock_order_item_repository: OrderItemRepository,
        order_item_dto: OrderItemDTO,
    ):
        """Testa que create_order_item propaga exceções do repositório."""
        mock_order_item_repository.create = AsyncMock(
            side_effect=Exception("Erro no banco de dados")
        )

        with pytest.raises(Exception) as exc_info:
            await order_item_service.create_order_item(order_item_dto)

        assert "Erro no banco de dados" in str(exc_info.value)
        mock_order_item_repository.create.assert_called_once_with(order_item_dto)

    @pytest.mark.asyncio
    async def test_create_order_item_with_large_quantity(
        self,
        order_item_service: OrderItemService,
        mock_order_item_repository: OrderItemRepository,
    ):
        """Testa que create_order_item aceita quantidades grandes."""
        order_item_dto = OrderItemDTO(
            product_id=1,
            quantity=1000,
            price=50.00,
        )
        order_item_response = OrderItemResponseDTO(
            id=1,
            order_id=1,
            product_id=1,
            quantity=1000,
            price=50.00,
        )
        mock_order_item_repository.create = AsyncMock(return_value=order_item_response)

        response = await order_item_service.create_order_item(order_item_dto)

        assert response.quantity == 1000
        mock_order_item_repository.create.assert_called_once_with(order_item_dto)

    @pytest.mark.asyncio
    async def test_create_order_item_with_high_price(
        self,
        order_item_service: OrderItemService,
        mock_order_item_repository: OrderItemRepository,
    ):
        """Testa que create_order_item aceita preços altos."""
        order_item_dto = OrderItemDTO(
            product_id=1,
            quantity=1,
            price=9999.99,
        )
        order_item_response = OrderItemResponseDTO(
            id=1,
            order_id=1,
            product_id=1,
            quantity=1,
            price=9999.99,
        )
        mock_order_item_repository.create = AsyncMock(return_value=order_item_response)

        response = await order_item_service.create_order_item(order_item_dto)

        assert response.price == 9999.99
        mock_order_item_repository.create.assert_called_once_with(order_item_dto)

    @pytest.mark.asyncio
    async def test_create_order_item_with_decimal_price(
        self,
        order_item_service: OrderItemService,
        mock_order_item_repository: OrderItemRepository,
    ):
        """Testa que create_order_item aceita preços com decimais."""
        order_item_dto = OrderItemDTO(
            product_id=1,
            quantity=3,
            price=19.99,
        )
        order_item_response = OrderItemResponseDTO(
            id=1,
            order_id=1,
            product_id=1,
            quantity=3,
            price=19.99,
        )
        mock_order_item_repository.create = AsyncMock(return_value=order_item_response)

        response = await order_item_service.create_order_item(order_item_dto)

        assert response.price == 19.99
        assert response.quantity == 3
        mock_order_item_repository.create.assert_called_once_with(order_item_dto)

    @pytest.mark.asyncio
    async def test_create_order_item_missing_product_id(
        self,
        order_item_service: OrderItemService,
    ):
        """Testa que create_order_item valida product_id ausente."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            OrderItemDTO(
                quantity=2,
                price=50.00,
            )

    @pytest.mark.asyncio
    async def test_create_order_item_missing_quantity(
        self,
        order_item_service: OrderItemService,
    ):
        """Testa que create_order_item valida quantity ausente."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            OrderItemDTO(
                product_id=1,
                price=50.00,
            )

    @pytest.mark.asyncio
    async def test_create_order_item_missing_price(
        self,
        order_item_service: OrderItemService,
    ):
        """Testa que create_order_item valida price ausente."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            OrderItemDTO(
                product_id=1,
                quantity=2,
            )

    @pytest.mark.asyncio
    async def test_create_order_item_with_string_product_id(
        self,
        order_item_service: OrderItemService,
    ):
        """Testa que create_order_item valida tipo de product_id."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            OrderItemDTO(
                product_id="abc",
                quantity=2,
                price=50.00,
            )
