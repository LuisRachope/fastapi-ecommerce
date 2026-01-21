from app.application.services.order_item_service import OrderItemService
from app.application.services.order_service import OrderService
from app.application.services.product_service import ProductService
from app.infrastructure.persistence.repositories.order_item_repository_impl import SQLOrderItemRepository
from app.infrastructure.persistence.repositories.order_repository_impl import SQLOrderRepository
from app.infrastructure.persistence.repositories.product_repository_impl import SQLProductRepository

class DependencyContainer:
    def __init__(self):
        self._repositories = {}
        self._services = {}
        self._initialize_repositories()
        self._initialize_services()

    def _initialize_repositories(self):
        """Initialize all repositories as singletons"""
        self._repositories['product_repository'] = SQLProductRepository()
        self._repositories['order_repository'] = SQLOrderRepository()
        self._repositories['order_item_repository'] = SQLOrderItemRepository()
    
    def _initialize_services(self):
        """Initialize all services with repository dependencies"""
        self._services['product_service'] = ProductService(
            product_repository=self._repositories['product_repository']
        )

        self._services['order_service'] = OrderService(
            order_repository=self._repositories['order_repository'],
            order_item_repository=self._repositories['order_item_repository'],
        )

        self._services['order_item_service'] = OrderItemService(
            order_item_repository=self._repositories['order_item_repository'],
        )

    # Service getters
    def get_product_service(self) -> ProductService:
        return self._services['product_service']

    def get_order_service(self):
        return self._services['order_service']
    
    def get_order_item_service(self):
        return self._services['order_item_service']

# Global container instance
dependency_container = DependencyContainer()


# FastAPI dependency functions
def get_product_service() -> ProductService:
    return dependency_container.get_product_service()

def get_order_service() -> OrderService:
    return dependency_container.get_order_service()

def get_order_item_service() -> OrderItemService:
    return dependency_container.get_order_item_service()