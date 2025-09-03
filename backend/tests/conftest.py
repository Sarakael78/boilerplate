"""
Test configuration and utilities.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..app.main import app
from ..app.db.database import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture
def test_db():
    """Provide test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_client():
    """Provide test client."""
    return client
