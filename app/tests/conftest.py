from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.domain.entities.product_entity import ProductEntity


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


@pytest.fixture
def patched_async_session(mocker):
    """
    Fixture que faz patch automático do async_session.
    Elimina a necessidade de usar patch() manualmente nos testes.
    Use isso para simplificar testes de repositório.
    """
    mock = MagicMock()
    mock.__aenter__.return_value = AsyncMock()
    mock.__aexit__.return_value = None

    mocker.patch(
        "app.infrastructure.persistence.repositories.product_repository_impl.async_session",
        return_value=mock,
    )
    return mock
