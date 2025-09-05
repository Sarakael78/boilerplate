"""
Base repository pattern implementation.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Any

from sqlalchemy.orm import Session

# Generic type for the model
T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository class providing common CRUD operations.
    """

    def __init__(self, db: Session, model: type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, id: Any) -> Optional[T]:
        """Get an entity by its ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[T]:
        """Get all entities."""
        return self.db.query(self.model).all()

    def create(self, **kwargs) -> T:
        """Create a new entity."""
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, instance: T, **kwargs) -> T:
        """Update an existing entity."""
        for key, value in kwargs.items():
            setattr(instance, key, value)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, instance: T) -> None:
        """Delete an entity."""
        self.db.delete(instance)
        self.db.commit()

    def get_by_field(self, field_name: str, value: Any) -> Optional[T]:
        """Get an entity by a specific field."""
        return self.db.query(self.model).filter(getattr(self.model, field_name) == value).first()

    def get_many_by_field(self, field_name: str, value: Any) -> List[T]:
        """Get multiple entities by a specific field."""
        return self.db.query(self.model).filter(getattr(self.model, field_name) == value).all()
