from abc import ABC, abstractmethod
from typing import Any, Dict, List, TypeVar, Generic, Optional

T = TypeVar('T')

class IBaseRepository(Generic[T], ABC):
    """Interface for base repository operations"""
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities"""
        pass
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> T:
        """Create a new entity"""
        pass
    
    @abstractmethod
    def update(self, entity: T, data: Dict[str, Any]) -> T:
        """Update an existing entity"""
        pass
    
    @abstractmethod
    def delete(self, entity: T) -> None:
        """Delete an entity"""
        pass