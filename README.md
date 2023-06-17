# The hrbot
The hrbot is a wrapper on top of the [HighRise Python Bot SDK](https://github.com/pocketzworld/python-bot-sdk) that makes it easy to create bots in [HighRise](https://highrise.game/).

Install the library:
```shell
pip install hrbot
```

Example:
```python
from hrbot import Bot, Dispatcher  
from hrbot.types.hr import *

dp = Dispatcher()
bot = Bot(
    api_key='',
    room_id='',
    dispatcher=dp
)

@dp.on_user_join()
async def user_join(user: User):
    await bot.highrise.chat(f'Hi, {user.username}')

@dp.on_chat(command='help', case_ignore=True, prefix='!')
async def help_command(user: User, message: str):
    await bot.highrise.chat('some text')

@dp.on_chat()
async def echo(user: User, message: str):
    await bot.highrise.chat(message)

@dp.on_user_leave()
async def user_leave(user: User):
    await bot.highrise.chat(f'Goodbye, {user.username}')

if __name__ == '__main__':
    bot.start()
```