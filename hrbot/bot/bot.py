from .base import BaseBot
from ..types import _bcolors
from ..types.hr import SessionMetadata, User, Position, AnchorPosition, Reaction, CurrencyItem, Item
from typing import Literal
from quattro import TaskGroup

class Bot(BaseBot):
    @staticmethod
    def __event_handler(func):
        async def wrapper(self, *args, **kwargs):
            event_name = func.__name__
            await func(self, *args, **kwargs)
            await self.dp._process_event(event_name, *args, **kwargs)

        return wrapper

    @__event_handler
    async def before_start(self, tg: TaskGroup) -> None:
        """Called before the bot starts."""
        pass

    @__event_handler
    async def on_start(self, session_metadata: SessionMetadata) -> None:
        """On a connection to the room being established.

        This may be called multiple times, since the connection may be dropped
        and reestablished.
        """
        self.id = session_metadata.user_id

        print(
            f'{_bcolors.WARNING}Bot started in room: '
            f'{_bcolors.FAIL}{session_metadata.room_info.room_name}{_bcolors.ENDC}'
        )
        if self._detailed_start_message:
            print(
                f'{_bcolors.WARNING}user_id:             {_bcolors.FAIL}{session_metadata.user_id}{_bcolors.ENDC}\n'
                f'{_bcolors.WARNING}sdk_version:         {_bcolors.FAIL}{session_metadata.sdk_version}{_bcolors.ENDC}\n'
                f'{_bcolors.WARNING}rate_limits:         {_bcolors.FAIL}{session_metadata.rate_limits}{_bcolors.ENDC}\n'
                f'{_bcolors.WARNING}connection_id:       {_bcolors.FAIL}{session_metadata.connection_id}{_bcolors.ENDC}\n'
                f'{_bcolors.WARNING}owner_id:            {_bcolors.FAIL}{session_metadata.room_info.owner_id}{_bcolors.ENDC}\n'
            )

    @__event_handler
    async def on_chat(self, user: User, message: str) -> None:
        """On a received room-wide chat."""
        pass

    @__event_handler
    async def on_whisper(self, user: User, message: str) -> None:
        """On a received room whisper."""
        pass

    @__event_handler
    async def on_emote(self, user: User, emote_id: str, receiver: User | None) -> None:
        """On a received emote."""
        pass

    @__event_handler
    async def on_reaction(self, user: User, reaction: Reaction, receiver: User) -> None:
        """Called when someone reacts in the room."""
        pass

    @__event_handler
    async def on_user_join(self, user: User) -> None:
        """On a user joining the room."""
        pass

    @__event_handler
    async def on_user_leave(self, user: User) -> None:
        """On a user leaving the room."""
        pass

    @__event_handler
    async def on_tip(
            self, sender: User, receiver: User, tip: CurrencyItem | Item
    ) -> None:
        """On a tip received in the room."""
        pass

    @__event_handler
    async def on_channel(self, sender_id: str, message: str, tags: set[str]) -> None:
        """On a hidden channel message."""
        pass

    @__event_handler
    async def on_user_move(
            self, user: User, destination: Position | AnchorPosition
    ) -> None:
        """On a user moving in the room."""
        pass

    @__event_handler
    async def on_voice_change(
        self, users: list[tuple[User, Literal["voice", "muted"]]], seconds_left: int
    ) -> None:
        """On a change in voice status in the room."""
        pass

    @__event_handler
    async def on_message(
        self, user_id: str, conversation_id: str, is_new_conversation: bool
    ) -> None:
        """On a inbox message received from a user."""
        pass
