from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.core.exceptions import CategoryNotFoundError, DuplicateNameError
from app.utils.slug import normalize_slug



def test_create_category_generates_slug(db_session):
    service = CategoryService(db_session)
    payload = CategoryCreate(name="Books", description="All books")
    category = service.create(payload)
    assert category.id is not None
    assert category.slug == normalize_slug("Books")


def test_create_category_duplicate_name(db_session):
    service = CategoryService(db_session)
    service.create(CategoryCreate(name="Books"))
    try:
        service.create(CategoryCreate(name="Books"))
        assert False, "Expected DuplicateNameError"
    except DuplicateNameError:
        pass


def test_create_category_duplicate_slug_increments(db_session):
    service = CategoryService(db_session)
    # First category with explicit slug
    service.create(CategoryCreate(name="Books", slug="shared"))
    # Second with different name but same desired slug triggers increment logic
    cat2 = service.create(CategoryCreate(name="Novels", slug="shared"))
    assert cat2.slug == "shared-2"


def test_get_category_not_found(db_session):
    service = CategoryService(db_session)
    try:
        service.get_by_id(999)
        assert False, "Expected CategoryNotFoundError"
    except CategoryNotFoundError:
        pass


def test_update_partial(db_session):
    service = CategoryService(db_session)
    cat = service.create(CategoryCreate(name="Books"))
    updated = service.update_partial(cat.id, CategoryUpdate(description="Updated desc"))
    assert updated.description == "Updated desc"
    assert updated.name == "Books"


def test_delete_category(db_session):
    service = CategoryService(db_session)
    cat = service.create(CategoryCreate(name="Books"))
    service.delete(cat.id)
    try:
        service.get_by_id(cat.id)
        assert False, "Expected CategoryNotFoundError after delete"
    except CategoryNotFoundError:
        pass
