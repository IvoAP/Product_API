from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    # Query helpers
    def get_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_slug(self, slug: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.slug == slug).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name == name).first()

    def list_all(self) -> List[Category]:
        return self.db.query(Category).order_by(Category.id.asc()).all()

    def exists_slug(self, slug: str, exclude_id: int | None = None) -> bool:
        q = self.db.query(Category).filter(Category.slug == slug)
        if exclude_id:
            q = q.filter(Category.id != exclude_id)
        return self.db.query(q.exists()).scalar()

    def exists_name(self, name: str, exclude_id: int | None = None) -> bool:
        q = self.db.query(Category).filter(Category.name == name)
        if exclude_id:
            q = q.filter(Category.id != exclude_id)
        return self.db.query(q.exists()).scalar()

    # Persistence helpers
    def add(self, category: Category) -> None:
        self.db.add(category)

    def delete(self, category: Category) -> None:
        self.db.delete(category)

    def commit_and_refresh(self, category: Category) -> Category:
        self.db.commit()
        self.db.refresh(category)
        return category
