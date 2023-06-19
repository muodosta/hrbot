from hrbot import Bot, Dispatcher
from hrbot.types.hr import User

dp = Dispatcher()
bot = Bot(
    api_key='',
    room_id='',
    dispatcher=dp
)
"""
if case_ignore=True the handler will process messages case insensitive
This will all work: Text, TEXT, teXT, TeXt

prefix='.!#' means that the first character of the string 
must be one of the characters from .!#. 
This will all work: .start, !start, #start. 
The default is '/.!$#'.
"""
@dp.on_chat(command='start', case_ignore=True)
async def start_command(user: User, message: str):
    await bot.highrise.chat("Some text for start command")

@dp.on_chat(command=['emote', 'dance'], case_ignore=True, prefix='.!')
async def emote(user: User, message: str):
    await bot.highrise.chat("Some text for emote command")

@dp.on_chat(message=['hi', 'hello'], case_ignore=True)
async def hi(user: User, message: str):
    await bot.highrise.chat(f"Hi, {user.username}")

@dp.on_chat(regex='^(Test regex)')
async def regex_test(user: User, message: str):
    await bot.highrise.chat("Regex test")

@dp.on_chat(lambda message: message.lower().startswith('test'))
async def lambda_test(user: User, message: str):
    await bot.highrise.chat("Lambda test")

@dp.on_whisper()
async def whisper_echo(user: User, message: str):
    await bot.highrise.send_whisper(user.id, message)

@dp.on_chat()
async def chat_echo(user: User, message: str):
    await bot.highrise.chat(message)

if __name__ == '__main__':
    bot.start()
