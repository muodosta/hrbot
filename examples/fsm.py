import re

from asyncio import sleep as asleep
from hrbot import Bot, Dispatcher, fsm
from hrbot.types.hr import *

storage = fsm.storage.Memory()
dp = Dispatcher(fsm_storage=storage)
bot = Bot(
    api_key='',
    room_id='',
    dispatcher=dp
)


@dp.on_start()
async def start(session_metadata: SessionMetadata):
    print('Bot started')

@dp.on_user_join()
async def user_join(user: User):
    await asleep(2)
    await bot.highrise.chat(f'Hello, {user.username}! Write .start to register')


@dp.on_user_leave()
async def user_leave(user: User):
    await bot.highrise.chat(f'Goodbye, {user.username}')


class RegStates:
    name = 'reg.name'
    age = 'reg.age'
    gender = 'reg.gender'


class Registration:
    @staticmethod
    @dp.on_chat(command='start', case_ignore=True, prefix='.', state=None)
    async def start_reg(user: User, message: str):
        await bot.state.set_state(user.id, RegStates.name)
        await bot.highrise.chat(f'Write your name (only use the letters A-Z a-z and numbers):')

    @staticmethod
    @dp.on_chat(lambda m: 15 >= len(m) >= 2, regex='[a-zA-Z0-9]+', state=RegStates.name)
    async def reg_name(user: User, message: str):
        async with bot.state.data(user.id) as data:
            data['name'] = message
        await bot.state.set_state(user.id, RegStates.age)
        await bot.highrise.chat(f'Good, now write your age:')

    @staticmethod
    @dp.on_chat(state=RegStates.name)
    async def bad_reg_name(user: User, message: str):
        bad_message = 'Bad name'
        if not (15 >= len(message) >= 2):
            bad_message += ', the length must be more than 1 and less than 16 characters'
        if not re.fullmatch(r'[a-zA-Z0-9]+', message):
            bad_message += ', can only use the letters A-Z a-z and numbers'
        await bot.highrise.chat(bad_message + '. Write again:')

    @staticmethod
    @dp.on_chat(lambda m: m.isdigit() and 18 < int(m), state=RegStates.age)
    async def reg_age(user: User, message: str):
        async with bot.state.data(user.id) as data:
            data['age'] = message
        await bot.state.set_state(user.id, RegStates.gender)
        await bot.highrise.chat(f'Good, now write your gender (write w/m)')

    @staticmethod
    @dp.on_chat(state=RegStates.age)
    async def bad_reg_age(user: User, message: str):
        bad_message = 'Bad age'
        if not message.isdigit():
            bad_message += ', this is not a number'
        elif not (int(message) >= 18):
            bad_message += ', only 18+'
        await bot.highrise.chat(bad_message + '. Write again:')

    @staticmethod
    @dp.on_chat(message=['m', 'man', 'w', 'woman'], case_ignore=True, state=RegStates.gender)
    async def reg_sex(user: User, message: str):
        async with bot.state.data(user.id) as data:
            await bot.highrise.chat(
                f'Your profile:\n'
                f'-name:{data["name"]}\n'
                f'-age:{data["age"]}\n'
                f'-gender:{message.lower()}'
            )
        await bot.state.finish(user.id)

    @staticmethod
    @dp.on_chat(state=RegStates.gender)
    async def bad_reg_sex(user: User, message: str):
        await bot.highrise.chat(f'Bad gender, write w/m')


@dp.on_chat()
async def echo(user: User, message: str):
    await bot.highrise.chat(f'{message}, for {user.username}')

if __name__ == '__main__':
    bot.start()
