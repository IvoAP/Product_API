from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryService
from app.core.exceptions import (
    CategoryNotFoundError,
    DuplicateSlugError,
    DuplicateNameError,
)

router = APIRouter(prefix="/categories", tags=["categories"])

def get_service(db: Session) -> CategoryService:
    return CategoryService(db)

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    service = get_service(db)
    try:
        return service.create(payload)
    except DuplicateSlugError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except DuplicateNameError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/", response_model=List[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    service = get_service(db)
    return service.list_all()

@router.get("/by-name/{name}", response_model=CategoryRead)
def get_category_by_name(name: str, db: Session = Depends(get_db)):
    service = get_service(db)
    try:
        return service.get_by_name(name)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/by-slug/{slug}", response_model=CategoryRead)
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    service = get_service(db)
    try:
        return service.get_by_slug(slug)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{category_id}", response_model=CategoryRead)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    service = get_service(db)
    try:
        return service.get_by_id(category_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{category_id}", response_model=CategoryRead)
def replace_category(category_id: int, payload: CategoryCreate, db: Session = Depends(get_db)):
    service = get_service(db)
    try:
        return service.replace(category_id, payload)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DuplicateSlugError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except DuplicateNameError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    service = get_service(db)
    try:
        return service.update_partial(category_id, payload)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DuplicateSlugError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except DuplicateNameError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    service = get_service(db)
    try:
        service.delete(category_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None
