from sqlalchemy.orm import Session
from app.db.models import Category
from app.utils.slug import normalize_slug

DEFAULT_CATEGORIES = [
    {"name": "Books", "description": "Books and reading materials", "slug": "books"},
    {"name": "Electronics", "description": "Electronic devices and gadgets", "slug": "electronics"},
    {"name": "Clothing", "description": "Apparel and accessories", "slug": "clothing"},
]

def seed_initial_categories(db: Session) -> None:
    """Ensure at least the default categories exist.

    Idempotent: only inserts missing ones by slug.
    """
    existing = {c.slug for c in db.query(Category).all()}
    created_any = False
    for cat in DEFAULT_CATEGORIES:
        slug = cat["slug"] or normalize_slug(cat["name"])
        if slug not in existing:
            db.add(Category(name=cat["name"], slug=slug, description=cat["description"]))
            created_any = True
    if created_any:
        db.commit()
