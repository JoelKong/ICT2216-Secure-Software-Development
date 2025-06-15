from app.db import db
from flask import current_app
from app.interfaces.repositories.IBaseRepository import IBaseRepository
from typing import TypeVar, Dict, List, Optional, Any, Generic

T = TypeVar('T')

class BaseRepository(IBaseRepository[T], Generic[T]):
    """Base repository class providing common database operations"""
    
    def __init__(self, model):
        self.model = model
        self.db = db
        
    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID"""
        try:
            return self.model.query.get(id)
        except Exception as e:
            current_app.logger.error(f"Error retrieving {self.model.__name__} with ID {id}: {str(e)}")
            raise
    
    def get_all(self) -> List[T]:
        """Get all entities"""
        try:
            return self.model.query.all()
        except Exception as e:
            current_app.logger.error(f"Error retrieving all {self.model.__name__}: {str(e)}")
            raise
    
    def create(self, data: Dict[str, Any]) -> T:
        """Create a new entity"""
        try:
            entity = self.model(**data)
            db.session.add(entity)
            db.session.commit()
            return entity
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise
    
    def update(self, entity: T, data: Dict[str, Any]) -> T:
        """Update an existing entity"""
        try:
            for key, value in data.items():
                setattr(entity, key, value)
            db.session.commit()
            return entity
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating {self.model.__name__}: {str(e)}")
            raise
    
    def delete(self, entity: T) -> None:
        """Delete an entity"""
        try:
            db.session.delete(entity)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error deleting {self.model.__name__}: {str(e)}")
            raise