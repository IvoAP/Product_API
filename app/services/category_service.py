from typing import Optional, List
from sqlalchemy.orm import Session

from app.db.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.repositories.category_repository import CategoryRepository
from app.core.exceptions import (
    CategoryNotFoundError,
    DuplicateSlugError,
    DuplicateNameError,
)
from app.utils.slug import generate_unique_slug, normalize_slug

class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)
        self.db = db

    # Read operations
    def list_all(self) -> List[Category]:
        return self.repo.list_all()

    def get_by_id(self, category_id: int) -> Category:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)
        return category

    def get_by_slug(self, slug: str) -> Category:
        category = self.repo.get_by_slug(slug)
        if not category:
            raise CategoryNotFoundError(slug)
        return category

    def get_by_name(self, name: str) -> Category:
        category = self.repo.get_by_name(name)
        if not category:
            raise CategoryNotFoundError(name)
        return category

    # Create
    def create(self, payload: CategoryCreate) -> Category:
        slug = payload.slug or normalize_slug(payload.name)
        # Ensure uniqueness / generate incremented slug if needed
        existing_slugs = {c.slug for c in self.repo.list_all()}
        if slug in existing_slugs:
            slug = generate_unique_slug(payload.name, existing_slugs)
        if self.repo.exists_name(payload.name):
            raise DuplicateNameError(payload.name)
        category = Category(name=payload.name, slug=slug, description=payload.description)
        self.repo.add(category)
        return self.repo.commit_and_refresh(category)

    # Replace (PUT)
    def replace(self, category_id: int, payload: CategoryCreate) -> Category:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)

        slug = payload.slug or normalize_slug(payload.name)
        if self.repo.exists_slug(slug, exclude_id=category.id):
            raise DuplicateSlugError(slug)
        if self.repo.exists_name(payload.name, exclude_id=category.id):
            raise DuplicateNameError(payload.name)

        category.name = payload.name
        category.slug = slug
        category.description = payload.description
        return self.repo.commit_and_refresh(category)

    # Partial update (PATCH)
    def update_partial(self, category_id: int, payload: CategoryUpdate) -> Category:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)

        if payload.name is not None:
            if self.repo.exists_name(payload.name, exclude_id=category.id):
                raise DuplicateNameError(payload.name)
            category.name = payload.name
        if payload.slug is not None:
            slug = normalize_slug(payload.slug)
            if self.repo.exists_slug(slug, exclude_id=category.id):
                raise DuplicateSlugError(slug)
            category.slug = slug
        if payload.description is not None:
            category.description = payload.description

        return self.repo.commit_and_refresh(category)

    # Delete
    def delete(self, category_id: int) -> None:
        category = self.repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)
        self.repo.delete(category)
        self.db.commit()
