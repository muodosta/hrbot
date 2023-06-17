import asyncio
import traceback

from highrise import __main__ as __hr_main__
from highrise import BaseBot as HrBaseBot
from ..dispatcher.dispatсher import Dispatcher


class BaseBot(HrBaseBot):

    def __init__(
            self,
            api_key: str,
            room_id: str,
            dispatcher: Dispatcher
    ):
        self.api_key = api_key
        self.room_id = room_id
        self.dp = dispatcher
        self.state = self.dp.state

    def start(
            self,
            skip_exception=False,
            detailed_start_message=True
    ):
        self._detailed_start_message = detailed_start_message

        try:
            bots = [__hr_main__.BotDefinition(bot=self, api_token=self.api_key, room_id=self.room_id)]
            asyncio.run(__hr_main__.main(bots))
        except (KeyboardInterrupt, SystemExit):
            # loop.stop()
            pass
        finally:
            print("\nGoodbye!\N{ALIEN MONSTER}")
