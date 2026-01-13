from app.application.services.product_service import ProductService
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
    
    def _initialize_services(self):
        """Initialize all services with repository dependencies"""
        self._services['product_service'] = ProductService(
            product_repository=self._repositories['product_repository']
        )

    # Service getters
    def get_product_service(self) -> ProductService:
        return self._services['product_service']


# Global container instance
dependency_container = DependencyContainer()


# FastAPI dependency functions
def get_product_service() -> ProductService:
    return dependency_container.get_product_service()
