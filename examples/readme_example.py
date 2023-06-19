from hrbot import Bot, Dispatcher
from hrbot.types.hr import User

dp = Dispatcher()
bot = Bot(
    api_key='',
    room_id='',
    dispatcher=dp
)

@dp.on_user_join()
async def user_join(user: User):
    """Triggers when a player joins a room"""
    await bot.highrise.chat(f'Hi, {user.username}')

@dp.on_user_leave()
async def user_leave(user: User):
    """Triggers when a player leaves the room"""
    await bot.highrise.chat(f'Goodbye, {user.username}')

@dp.on_chat(command='help', case_ignore=True, prefix='.!')
async def help_command(user: User, message: str):
    """Works for .help and !help messages. Not case-sensitive"""
    await bot.highrise.chat("Some text for help command")

@dp.on_chat()
async def echo(user: User, message: str):
    """Works for all chat messages"""
    await bot.highrise.chat(message)

if __name__ == '__main__':
    bot.start()
