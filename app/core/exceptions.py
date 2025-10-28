class CategoryNotFoundError(Exception):
    def __init__(self, identifier: str | int):
        super().__init__(f"Category not found: {identifier}")
        self.identifier = identifier

class DuplicateSlugError(Exception):
    def __init__(self, slug: str):
        super().__init__(f"Slug already exists: {slug}")
        self.slug = slug

class DuplicateNameError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Name already exists: {name}")
        self.name = name
