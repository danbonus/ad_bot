import typing

from vkbottle_overrides.tools.dev_tools.ctx_tool import BaseContext
from .abc import ABCStorage


class CtxStorage(ABCStorage, BaseContext):
    """ Context storage
    Documentation: https://github.com/timoniq/vkbottle/blob/master/docs/tools/storage.md
    """

    storage: dict = {}

    def __init__(
        self, default: dict = None, force_reset: bool = False, section=None
    ):

        default = default or {}
        if not self.get_instance() or force_reset:
            self.storage = default
            self.set_instance(self)

        self.section = "default" if not section else section

        if self.section not in self.get_instance().storage:
            self.get_instance().storage[self.section] = {}

    def set(self, key: typing.Hashable, value: typing.Any) -> None:
        current_storage = self.get_instance().storage
        current_storage[self.section][key] = value
        self.set_instance(CtxStorage(current_storage, True))

    def update(self, key: typing.Hashable, **info) -> None:
        current_storage = self.get_instance().storage

        old_value = self.get(key)
        old_value.update(info)

        current_storage[self.section][key] = old_value
        self.set_instance(CtxStorage(current_storage, True))

    def get(self, key: typing.Hashable) -> typing.Any:
        return self.get_instance().storage.get(self.section)[key]

    def delete(self, key: typing.Hashable) -> None:
        new_storage = self.get_instance().storage
        new_storage[self.section].pop(key)
        self.set_instance(CtxStorage(new_storage, True))

    def contains(self, key: typing.Hashable) -> bool:
        return key in self.get_instance().storage[self.section]
