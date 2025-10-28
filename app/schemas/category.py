from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator
import re

_slug_regex = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name must not be empty")
        if len(v) > 100:
            raise ValueError("name exceeds 100 characters")
        return v

class CategoryCreate(CategoryBase):
    slug: Optional[str] = None  # may be auto-generated if absent

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip().lower()
        if not _slug_regex.match(v):
            raise ValueError("invalid slug: use only a-z0-9 and hyphens, no consecutive spaces")
        if len(v) > 120:
            raise ValueError("slug exceeds 120 characters")
        return v

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v2 = v.strip()
        if not v2:
            raise ValueError("name must not be empty")
        if len(v2) > 100:
            raise ValueError("name exceeds 100 characters")
        return v2

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v2 = v.strip().lower()
        if not _slug_regex.match(v2):
            raise ValueError("invalid slug: use only a-z0-9 and hyphens")
        if len(v2) > 120:
            raise ValueError("slug exceeds 120 characters")
        return v2

class CategoryRead(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
