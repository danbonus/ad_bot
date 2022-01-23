from typing import Any, Hashable

from .ctx_tool import BaseContext
from .abc import ABCStorage


class CtxStorage(ABCStorage, BaseContext):
    storage: dict = {}

    def __init__(
        self, 
        default: dict = None, 
        force_reset: bool = False,
        section=None
    ):

        default = default or {}
        if not self.get_instance() or force_reset:
            self.storage = default
            self.set_instance(self)

        self.section = "default" if not section else section

        if self.section not in self.get_instance().storage:
            self.get_instance().storage[self.section] = {}

    def set(self, key: Hashable, value: Any) -> None:
        current_storage = self.get_instance().storage
        current_storage[self.section][key] = value
        self.set_instance(CtxStorage(current_storage, True))

    def update(self, key: Hashable, **info) -> None:
        current_storage = self.get_instance().storage

        old_value = self.get(key)
        old_value.update(info)

        current_storage[self.section][key] = old_value
        self.set_instance(CtxStorage(current_storage, True))

    def get(self, key: Hashable) -> Any:
        return self.get_instance().storage.get(self.section)[key]

    def delete(self, key: Hashable) -> None:
        new_storage = self.get_instance().storage
        new_storage[self.section].pop(key)
        self.set_instance(CtxStorage(new_storage, True))

    def contains(self, key: Hashable) -> bool:
        return key in self.get_instance().storage[self.section]
