import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from decimal import Decimal
from datetime import datetime

from app.domain.entities.product import ProductEntity


@pytest.fixture
def product_entity() -> ProductEntity:
    """Fixture for a sample ProductEntity."""
    return ProductEntity(
        id=str(uuid4()),
        name="Test Product",
        description="Test Description",
        price=Decimal("99.99"),
        quantity=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def product_entity_list() -> list[ProductEntity]:
    """Fixture for a list of ProductEntity objects."""
    return [
        ProductEntity(
            id=str(uuid4()),
            name=f"Product {i}",
            description=f"Description {i}",
            price=Decimal(f"{10 + i}.99"),
            quantity=i * 5,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        for i in range(1, 4)
    ]


@pytest.fixture
def mock_converter():
    """Fixture for mocked ProductConverter."""
    return MagicMock()


@pytest.fixture
def mock_session():
    """Fixture for mocked async session."""
    return AsyncMock()


@pytest.fixture
def mock_async_session_context(mock_session):
    """Fixture for mocked async_session context manager."""
    mock = AsyncMock()
    mock.__aenter__.return_value = mock_session
    mock.__aexit__.return_value = None
    return mock
