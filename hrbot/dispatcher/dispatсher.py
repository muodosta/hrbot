import importlib
import re

from .handler import HandlerFactory, DictWrapper, HandlerObj
from . import filter, fsm
from ..types import handler
from typing import Optional


class DispatcherEvents:
    def on_start(self):
        """On a connection to the room being established.

        This may be called multiple times, since the connection may be dropped
        and reestablished.
        """
        pass

    def on_chat(
            self,
            *custom_filter,
            user: handler.User = None,
            message: handler.Message = None,
            command: handler.Message = None,
            prefix: Optional[str] = handler.PrefixDefaultValue,
            case_ignore: Optional[bool] = handler.CaseIgnoreDefaultValue,
            regex: Optional[str] = None,
            state: Optional[str] = None,
            go_on: Optional[bool] = False,
            **kwargs
    ):
        """On a received room-wide chat."""
        pass

    def on_whisper(
            self,
            *custom_filter,
            user: handler.User = None,
            message: handler.Message = None,
            command: handler.Message = None,
            prefix: Optional[str] = handler.PrefixDefaultValue,
            case_ignore: Optional[bool] = handler.CaseIgnoreDefaultValue,
            regex: Optional[str] = None,
            state: Optional[str] = None,
            go_on: Optional[bool] = False,
            **kwargs
    ):
        """On a received room whisper."""
        pass

    def on_emote(
            self,
            *custom_filter,
            user: handler.User = None,
            emote_id: handler.Message = None,
            receiver: handler.User = None,
            state: Optional[str] = None,
            go_on: Optional[bool] = False,
            **kwargs
    ):
        """On a received emote."""
        pass

    def on_reaction(
            *custom_filter,
            user: handler.User = None,
            reaction: handler.Reaction = None,
            receiver: handler.User = None,
            state: Optional[str] = None,
            go_on: Optional[bool] = False,
            **kwargs
    ):
        """Called when someone reacts in the room."""
        pass

    def on_user_join(
            self,
            *custom_filter,
            user: handler.User = None,
            state: Optional[str] = None,
            go_on: Optional[bool] = False,
            **kwargs
    ):
        """On a user joining the room."""
        pass

    def on_user_leave(
            self,
            *custom_filter,
            user: handler.User = None,
            state: Optional[str] = None,
            go_on: Optional[bool] = False,
            **kwargs
    ):
        """On a user leaving the room."""
        pass

    def on_tip(
            *custom_filter,
            sender: handler.User = None,
            receiver: handler.User = None,
            tip: handler.Tip = None,
            state: Optional[str] = None,
            go_on: Optional[bool] = False,
            **kwargs
    ):
        """On a tip received in the room."""
        pass

    def on_channel(
            *custom_filter,
            sender_id: Optional[str] = None,
            message: handler.Message = None,
            tags: Optional[set[str]] = None,
            go_on: Optional[bool] = False,
            **kwargs
    ):
        """On a hidden channel message."""
        pass

    def on_user_move(
            *custom_filter,
            user: handler.User = None,
            destination: handler.Destination = None,
            state: Optional[str] = None,
            go_on: Optional[bool] = False,
            **kwargs
    ):
        """On a user moving in the room."""
        pass


class Dispatcher(DispatcherEvents):
    def __init__(
            self,
            fsm_storage: Optional[fsm.storage.BaseStorage] = None
    ):
        if not fsm_storage:
            fsm_storage = fsm.storage.Memory()
        self.state = fsm.state.FSMState(storage=fsm_storage)
        filter.Check.fsm = self.state

        self.__handlers: list[HandlerObj] = list()
        self.__handler_factory = HandlerFactory(handlers=self.__handlers)

    async def _process_event(self, handler_type: str, *args, **kwargs):
        await self.__handler_factory._process(handler_type, *args, **kwargs)

    @staticmethod
    def __pre_processing_handler_data(handler_data: dict) -> dict:
        if handler_data.get('regex', None):
            handler_data['regex'] = re.compile(handler_data['regex'])
        return handler_data

    def __getattribute__(self, method_name):
        bot_module = importlib.import_module('aiohr.bot.bot')
        if hasattr(bot_module.Bot, method_name):
            return self.__create_decorator(method_name)
        return super().__getattribute__(method_name)

    def __create_decorator(self, method_name):
        def wrapper(*custom_filter, **kwargs):
            kwargs = self.__pre_processing_handler_data(kwargs)

            def decorator(callback):
                # Обработка фильтров и создание обработчика
                self.__handlers.append(HandlerObj(
                    type=method_name,
                    filter_func=getattr(filter, method_name),
                    callback=callback,
                    custom_filters=custom_filter,
                    data=DictWrapper(kwargs, rise_exception=False)
                ))
                return callback

            return decorator

        return wrapper
