from typing import Any

from PyStore._utils import is_valid_document, parent_path
from PyStore.engines import PyStoreEngine
from PyStore.types import Json


class DocumentDelegate:

    def __init__(self, path: str, engine: PyStoreEngine):
        self.path = path
        self.engine = engine

    @property
    def id(self):
        return self.path.split('/')[-1]

    @property
    def exists(self) -> bool:
        return self.engine.path_exists(self.path) and is_valid_document(self.path) and self.engine.doc_exists(self.path)

    @property
    def parent(self):
        path = parent_path(self.path)
        if path:
            from PyStore.core._delegates.collection import CollectionDelegate
            return CollectionDelegate(path, self.engine)
        return None

    def collection(self, path: str):
        from PyStore.core._delegates.collection import CollectionDelegate
        return CollectionDelegate(f'{self.path}/{path}', self.engine)

    def set(self, data: Json):
        self.engine.set(self.path, data)

    def delete(self):
        self.engine.delete(self.path)

    def get(self):
        return DocumentDelegate(self.path, self.engine)

    def update(self, data: Json):
        self.engine.update(self.path, data)

    def get_field(self, field: str, default=None) -> Any:
        return self.engine.get_field(self.path, field, default)

    def data(self) -> Json | None:
        if self.exists:
            return self.engine.get_document(self.path)
        return None
