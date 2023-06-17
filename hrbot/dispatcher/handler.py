from typing import Callable, Optional
from dataclasses import dataclass
from .. import types


class DictWrapper:
    def __init__(
            self,
            data: dict,
            rise_exception=True,
            return_if_exception=None
    ):
        self._data = data
        self.rise_exception = rise_exception
        self.return_if_exception = return_if_exception

    def __getattr__(self, item):
        if item in self._data:
            return self._data[item]
        else:
            if self.rise_exception:
                raise AttributeError(f"`DictWrapper` object has no attribute '{item}'")
            return self.return_if_exception


@dataclass
class HandlerObj:
    type: str
    filter_func: Callable
    callback: Callable
    custom_filters: tuple
    data: DictWrapper


class HandlerFactory:
    def __init__(self, handlers: list[HandlerObj]):
        self.__handlers: list[HandlerObj] = handlers

    async def _process(self, handler_type: str, *args, **kwargs):
        for handler in self.__handlers:
            if handler.type == handler_type:
                if await handler.filter_func(handler, *args, **kwargs):
                    await handler.callback(*args, **kwargs)
                    if not handler.data.go_on:
                        break
