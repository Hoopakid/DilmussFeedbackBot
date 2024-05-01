import asyncio
import os
import logging

from aiogram import Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext

from Database.checking import is_user_authenticated, insert_user
from Database.datas import get_branch_data, get_team_id
from Keyboards.ReplyKeyboards import choose_time_btn, branch_btn, choose_team_btn, edit_user_data_btn
from Keyboards.InlineKeyboards import confirm_or_cancel_btn
from State.userState import UserState
from dispatcher import get_dispatcher

load_dotenv()

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get('BOT_TOKEN')

dp = get_dispatcher()
bot = Bot(BOT_TOKEN)


@dp.message(CommandStart())
async def start_bot(message: Message, state: FSMContext):
    first_name, last_name = '', ''
    if message.chat.first_name is not None:
        first_name = message.chat.first_name
    if message.chat.last_name is not None:
        last_name = message.chat.last_name
    await message.answer(
        f'Assalomu alaykum {first_name} {last_name}')
    user_chat_id = message.chat.id
    if is_user_authenticated(user_chat_id) is True:
        await message.answer('Botdagi yangiliklarni kuting')
    else:
        await message.answer('Ismingizni yuboring')
        await state.set_state(UserState.name)


@dp.message(UserState.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data({
        'name': message.text
    })
    await message.answer('Qaysi vaqtda ishlay olasiz?', reply_markup=choose_time_btn())
    await state.set_state(UserState.time)


@dp.message(UserState.time)
async def set_time(message: Message, state: FSMContext):
    await state.update_data({
        'time': message.text
    })
    await message.answer('Qaysi filial', reply_markup=branch_btn())
    await state.set_state(UserState.branch)


@dp.message(UserState.branch)
async def set_branch(message: Message, state: FSMContext):
    branch = message.text
    branch_id = get_branch_data(branch)
    branch_id = branch_id[0].get('id')
    await state.update_data({
        'branch': branch
    })
    branch_buttons = choose_team_btn(int(branch_id))
    await message.answer('Qaysi jamoa', reply_markup=branch_buttons)
    await state.set_state(UserState.team)


@dp.message(UserState.team)
async def confirm(message: Message, state: FSMContext):
    await state.update_data({
        'team': message.text
    })
    data = await state.get_data()
    name = data['name']
    branch = data['branch']
    time = data['time']

    branch_id = get_branch_data(branch)
    branch_id = branch_id[0].get('id')
    time_int = 0
    if time == 'Kechki 🌃':
        time_int = 2
    else:
        time_int = 1
    team = data['team']
    team_id = get_team_id(team)

    # updated
    time = time_int
    branch = branch_id
    team = team_id[0].get('id')
    finally_data = dict(
        name=str(name),
        branch_id=int(branch),
        time=int(time),
        team_id=int(team),
        user_chat_id=message.from_user.id,
    )
    insert_user(finally_data)
    await message.delete()
    await message.answer('Hurmatli mijoz yangiliklarni kuzatib turing')


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
