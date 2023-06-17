import re
from typing import Any, Callable, Optional

from . import fsm
from .handler import HandlerObj
from ..types import handler, hr, _bcolors


class Check:
    fsm: fsm.state.FSMState

    @staticmethod
    async def compare_two_value(
            handler: Any,
            event: Any,
            case_ignore: bool = False
    ) -> bool:
        """Checks the handler data with the event data.
        If the handler data is Null it returns True
        :param handler: Handler data
        :param event: Event data, can not take the value None
        :param case_ignore: Pass True to ignore the case of text
        :return: `True` if all checks have been completed,
        or handler equal to None, else `False`"""

        if handler:
            if case_ignore and hasattr(event, 'lower'):
                event = event.lower()
                new_handler = list()
                if isinstance(handler, (list, tuple, set)):
                    for i, handler_data in enumerate(handler):
                        new_handler.append(handler_data.lower())
                    handler = new_handler

            if isinstance(handler, (list, tuple, set)) and event not in handler:
                return False
            if not isinstance(handler, (list, tuple, set)) and not event == handler:
                return False
        return True

    @staticmethod
    async def state(user: hr.User, handler_filter: HandlerObj):
        handler_state = handler_filter.data.state

        if handler_state == '*':
            return True

        if 'state' in handler_filter.data._data.keys():
            if await Check.fsm.get_state(user.id) != handler_state:
                return False
        return True

    @staticmethod
    async def regex(handler_regex: re.Pattern | None, event_message: str) -> bool:
        if handler_regex and not handler_regex.fullmatch(event_message):
            return False
        return True

    @staticmethod
    async def func(event_param: Any, handler_func: Callable) -> bool:
        if handler_func(event_param):
            return True
        return False

    @staticmethod
    async def command(
            handler_commands: handler.Message,
            handler_prefix: Optional[str],
            event_message: str,
            case_ignore: bool = False
    ) -> bool:
        if not handler_commands:
            return True

        if case_ignore:
            event_message = event_message.lower()
            if isinstance(handler_commands, (list, tuple, set)):
                new_handler = list()
                for i, handler_command in enumerate(handler_commands):
                    new_handler.append(handler_command.lower())
                handler_commands = new_handler

        if event_message[0] not in handler_prefix:
            return False

        if event_message[1:] in handler_commands:
            return True
        return False


async def on_start(*args, **kwargs) -> bool: return True


async def on_chat(
        handler_filter: HandlerObj,
        user: hr.User,
        message: str,
        *args, **kwargs
) -> bool:
    if not await Check.state(user, handler_filter): return False
    if not await Check.compare_two_value(handler_filter.data.user, user): return False
    if not await Check.compare_two_value(handler_filter.data.message,
                                         message, handler_filter.data.case_ignore): return False
    if not await Check.command(handler_filter.data.command,
                               handler_filter.data.prefix if handler_filter.data.prefix else handler.PrefixDefaultValue,
                               message, handler_filter.data.case_ignore): return False
    if not await Check.regex(handler_filter.data.regex, message): return False
    for filter_func in handler_filter.custom_filters:
        if callable(filter_func) and not await Check.func(message, filter_func):
            return False
    return True


async def on_whisper(
        handler_filter: HandlerObj,
        user: hr.User,
        message: str,
        *args, **kwargs
) -> bool:
    if not await Check.state(user, handler_filter): return False
    if not await Check.compare_two_value(handler_filter.data.user, user): return False
    if not await Check.compare_two_value(handler_filter.data.message,
                                         message, handler_filter.data.case_ignore): return False
    if not await Check.command(handler_filter.data.command,
                               handler_filter.data.prefix if handler_filter.data.prefix else handler.PrefixDefaultValue,
                               message, handler_filter.data.case_ignore): return False
    if not await Check.regex(handler_filter.data.regex, message): return False
    for filter_func in handler_filter.custom_filters:
        if callable(filter_func) and not await Check.func(message, filter_func):
            return False
    return True


async def on_emote(
        handler_filter: HandlerObj,
        user: hr.User,
        emote_id: str,
        receiver: hr.User | None,
        *args, **kwargs
) -> bool:
    if not await Check.state(user, handler_filter): return False
    if not await Check.compare_two_value(handler_filter.data.user, user): return False
    if not await Check.compare_two_value(handler_filter.data.receiver, receiver): return False
    if not await Check.compare_two_value(handler_filter.data.emote_id, emote_id): return False
    for filter_func in handler_filter.custom_filters:
        if callable(filter_func) and not await Check.func(emote_id, filter_func):
            return False
    return True


async def on_reaction(
        handler_filter: HandlerObj,
        user: hr.User,
        reaction: hr.Reaction,
        receiver: hr.User | None,
        *args, **kwargs
) -> bool:
    if not await Check.state(user, handler_filter): return False
    if not await Check.compare_two_value(handler_filter.data.user, user): return False
    if not await Check.compare_two_value(handler_filter.data.receiver, receiver): return False
    if not await Check.compare_two_value(handler_filter.data.reaction, reaction): return False
    for filter_func in handler_filter.custom_filters:
        if callable(filter_func) and not await Check.func(reaction, filter_func):
            return False
    return True


async def on_user_join(
        handler_filter: HandlerObj,
        user: hr.User,
        *args, **kwargs
) -> bool:
    if not await Check.state(user, handler_filter): return False
    if not await Check.compare_two_value(handler_filter.data.user, user): return False
    for filter_func in handler_filter.custom_filters:
        if callable(filter_func) and not await Check.func(user, filter_func):
            return False
    return True


async def on_user_leave(
        handler_filter: HandlerObj,
        user: hr.User,
        *args, **kwargs
) -> bool:
    if not await Check.state(user, handler_filter): return False
    if not await Check.compare_two_value(handler_filter.data.user, user): return False
    for filter_func in handler_filter.custom_filters:
        if callable(filter_func) and not await Check.func(user, filter_func):
            return False
    return True


async def on_tip(
        handler_filter: HandlerObj,
        sender: hr.User,
        receiver: hr.User | None,
        tip: hr.CurrencyItem | hr.Item,
        *args, **kwargs
) -> bool:
    if not await Check.state(sender, handler_filter): return False
    if not await Check.compare_two_value(handler_filter.data.sender, sender): return False
    if not await Check.compare_two_value(handler_filter.data.receiver, receiver): return False
    if not await Check.compare_two_value(handler_filter.data.tip, tip): return False
    for filter_func in handler_filter.custom_filters:
        if callable(filter_func) and not await Check.func(tip, filter_func):
            return False
    return True


async def on_channel(
        handler_filter: HandlerObj,
        sender_id: str = None,
        message: str = None,
        tags: set[str] = None,
        *args, **kwargs
) -> bool:
    if not await Check.compare_two_value(handler_filter.data.sender_id, sender_id): return False
    if not await Check.compare_two_value(handler_filter.data.message, message): return False
    if not await Check.compare_two_value(handler_filter.data.tags, tags): return False
    for filter_func in handler_filter.custom_filters:
        if callable(filter_func) and not await Check.func(message, filter_func):
            return False
    return True


async def on_user_move(
        handler_filter: HandlerObj,
        user: hr.User,
        destination: hr.Position | hr.AnchorPosition,
        *args, **kwargs
) -> bool:
    if not await Check.state(user, handler_filter): return False
    if not await Check.compare_two_value(handler_filter.data.user, user): return False
    if not await Check.compare_two_value(handler_filter.data.destination, destination): return False
    for filter_func in handler_filter.custom_filters:
        if callable(filter_func) and not await Check.func(user, filter_func):
            return False
    return True
