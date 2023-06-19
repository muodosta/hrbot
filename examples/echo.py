from hrbot import Bot, Dispatcher
from hrbot.types.hr import User, Reaction, SessionMetadata

dp = Dispatcher()
bot = Bot(
    api_key='',
    room_id='',
    dispatcher=dp
)

@dp.on_chat()
async def chat_echo(user: User, message: str):
    """Works for all chat messages"""
    await bot.highrise.chat(message)

@dp.on_whisper()
async def whisper_echo(user: User, message: str):
    """Works for all whisper messages"""
    await bot.highrise.send_whisper(user.id, message)

@dp.on_reaction()
async def reaction_echo(user: User, reaction: Reaction, receiver: User):
    """Works for all reactions"""
    if not user.id == bot.id:  # Cannot send a reaction to yourself
        await bot.highrise.react(reaction, user.id)

if __name__ == '__main__':
    bot.start()
