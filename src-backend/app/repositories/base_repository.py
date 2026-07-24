from typing import Generic, TypeVar, Type, Any, Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, asc, desc, String, cast
from app.core.exceptions import handle_db_error, RecordNotFoundError

T = TypeVar("T")

class BaseRepository(Generic[T]):
    """
    Generic Repository Pattern base class handling CRUD transactions, pagination,
    filtering, dynamic sorting, search capability, and soft-delete filters.
    """
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, data: dict) -> T:
        """Create a new database row entry."""
        instance = self.model(**data)
        try:
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except Exception as e:
            self.db.rollback()
            raise handle_db_error(e)

    def get(self, id: Any, include_deleted: bool = False) -> Optional[T]:
        """Fetch a single record by its primary key ID."""
        query = self.db.query(self.model).filter(self.model.id == id)
        
        # Apply soft delete filter if column exists
        if hasattr(self.model, "is_deleted") and not include_deleted:
            query = query.filter(self.model.is_deleted == False)
            
        return query.first()

    def get_all(self, include_deleted: bool = False) -> List[T]:
        """Fetch all table records."""
        query = self.db.query(self.model)
        
        if hasattr(self.model, "is_deleted") and not include_deleted:
            query = query.filter(self.model.is_deleted == False)
            
        return query.all()

    def update(self, id: Any, data: dict) -> Optional[T]:
        """Update an existing record's details."""
        instance = self.get(id)
        if not instance:
            raise RecordNotFoundError(f"Record with ID {id} not found in database.")
            
        try:
            for key, val in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, val)
                    
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except Exception as e:
            self.db.rollback()
            raise handle_db_error(e)

    def delete(self, id: Any, soft: bool = True) -> bool:
        """
        Delete a database record. Performs soft delete by default if the model
        implements BaseModelMixin.is_deleted, otherwise hard deletes the row.
        """
        instance = self.get(id, include_deleted=True)
        if not instance:
            raise RecordNotFoundError(f"Record with ID {id} not found to delete.")
            
        try:
            if soft and hasattr(instance, "soft_delete"):
                instance.soft_delete()
            else:
                self.db.delete(instance)
                
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise handle_db_error(e)

    def find_one(self, filters: dict, include_deleted: bool = False) -> Optional[T]:
        """Find a single record matching specific criteria filters."""
        query = self.db.query(self.model)
        
        filter_clauses = []
        for key, val in filters.items():
            if hasattr(self.model, key):
                filter_clauses.append(getattr(self.model, key) == val)
                
        if hasattr(self.model, "is_deleted") and not include_deleted:
            filter_clauses.append(self.model.is_deleted == False)
            
        if filter_clauses:
            query = query.filter(and_(*filter_clauses))
            
        return query.first()

    def find_by(self, filters: dict, include_deleted: bool = False) -> List[T]:
        """Find all records matching specific criteria filters."""
        query = self.db.query(self.model)
        
        filter_clauses = []
        for key, val in filters.items():
            if hasattr(self.model, key):
                filter_clauses.append(getattr(self.model, key) == val)
                
        if hasattr(self.model, "is_deleted") and not include_deleted:
            filter_clauses.append(self.model.is_deleted == False)
            
        if filter_clauses:
            query = query.filter(and_(*filter_clauses))
            
        return query.all()

    def get_page(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: dict = None,
        sort_by: str = None,
        sort_order: str = "asc",
        search_query: str = None,
        search_columns: List[str] = None,
        include_deleted: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieves a paginated segment of records, applying search strings,
        property filters, sorting expressions, and soft-delete bounds.
        """
        query = self.db.query(self.model)
        
        # Apply standard filters
        filter_clauses = []
        if filters:
            for key, val in filters.items():
                if hasattr(self.model, key):
                    filter_clauses.append(getattr(self.model, key) == val)
                    
        if hasattr(self.model, "is_deleted") and not include_deleted:
            filter_clauses.append(self.model.is_deleted == False)
            
        if filter_clauses:
            query = query.filter(and_(*filter_clauses))
            
        # Apply Search Query (dynamic ILIKE wildcard mapping)
        if search_query and search_columns:
            search_clauses = []
            for col in search_columns:
                if hasattr(self.model, col):
                    column_attr = getattr(self.model, col)
                    # Convert to string and apply ILIKE/like pattern
                    search_clauses.append(cast(column_attr, String).ilike(f"%{search_query}%"))
            if search_clauses:
                query = query.filter(or_(*search_clauses))
                
        # Get count before offset limits
        total_records = query.count()
        
        # Apply Sorting
        if sort_by and hasattr(self.model, sort_by):
            col_attr = getattr(self.model, sort_by)
            order_func = desc if sort_order.lower() == "desc" else asc
            query = query.order_by(order_func(col_attr))
        elif hasattr(self.model, "created_at"):
            query = query.order_by(desc(self.model.created_at))
            
        # Apply Pagination Offsets
        offset = (page - 1) * page_size
        records = query.offset(offset).limit(page_size).all()
        
        total_pages = (total_records + page_size - 1) // page_size
        
        return {
            "records": records,
            "page": page,
            "page_size": page_size,
            "total_records": total_records,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
