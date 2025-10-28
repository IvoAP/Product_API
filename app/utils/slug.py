import re
from typing import Iterable

_slug_regex = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def normalize_slug(value: str) -> str:
    """Normalize a string into a slug candidate (lowercase, spaces to hyphens)."""
    return re.sub(r"\s+", "-", value.strip().lower())

def is_valid_slug(slug: str) -> bool:
    return bool(_slug_regex.match(slug))

def generate_unique_slug(base: str, existing: Iterable[str]) -> str:
    """Generate a unique slug from base against an iterable of existing slugs.

    Strategy: base -> base-2 -> base-3 ...
    existing is expected to be a collection (list/set) for O(1) membership ideally.
    """
    normalized = normalize_slug(base)
    if normalized not in existing:
        return normalized
    counter = 2
    while True:
        candidate = f"{normalized}-{counter}"
        if candidate not in existing:
            return candidate
        counter += 1
