from app.application.dtos.order_item_dto import OrderItemDTO, OrderItemResponseDTO
from app.domain.repositories.order_item_repository import OrderItemRepository


class OrderItemUseCase:
    """Use case para gerenciar itens de pedido."""

    def __init__(self, order_item_repository: OrderItemRepository):
        self.order_item_repository = order_item_repository

    async def create_order_item(self, order_item_data: OrderItemDTO) -> OrderItemResponseDTO:
        """Cria um novo item de pedido."""
        return await self.order_item_repository.create(order_item_data)
