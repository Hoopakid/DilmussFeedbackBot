import asyncio
import os
import requests
import logging
from datetime import datetime

from aiogram import Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext

from Database.checking import is_user_authenticated, insert_user, insert_data_to_base
from Database.datas import get_branch_data, get_team_id, get_user_name
from Keyboards.InlineKeyboards import yes_not_problem
from Keyboards.ReplyKeyboards import choose_time_btn, branch_btn, choose_team_btn, \
    assessment_for_user, problems_for_user, problem_other, problem_size, sizes_of_pants, size_of_dresses, kofta_sizes, \
    kelmagan_ishchilar
from State.userState import UserState, QuestionsState
from dispatcher import get_dispatcher

load_dotenv()

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('GROUP_ID')

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
    await message.answer("Ro'yhatdan o'tish muvaffaqiyatli yakunlandi. Botdagi yangiliklarni kuzatib turing.")


@dp.callback_query(lambda callback_query: callback_query.data == 'start')
async def start_questions(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer('Ish kunini baholang (1 - 10)', reply_markup=assessment_for_user())
    await state.set_state(QuestionsState.work)


# second part
@dp.message(QuestionsState.work)
async def get_mark_for_day_from_user(message: Message, state: FSMContext):
    await state.update_data({
        'work': message.text,
        'status': 'False'
    })
    await message.answer('Ish kunidagi muammolar', reply_markup=problems_for_user())
    await state.set_state(QuestionsState.problems)


@dp.message(QuestionsState.problems)
async def problems_user(message: Message, state: FSMContext):
    if message.text == "Boshqa ishga fokus bo'lishi":
        await state.update_data({
            'problems': message.text
        })
        await message.answer("Boshqa ishga fokus bo'lishi", reply_markup=problem_other())
        await state.set_state(QuestionsState.problem_another_work)
    elif message.text == "Razmer yo'q":
        await state.update_data({
            'problems': message.text
        })
        await message.answer("Qaysi kiyim uchun razmer qo'shilishini xohlaysiz?", reply_markup=problem_size())
        await state.set_state(QuestionsState.razmer)
    elif message.text == "Jamoa a'zolari kelmadi":
        await state.update_data({
            'problems': message.text
        })
        await message.answer("Jamoa a'zolaridan nechchi kishi bugun kelmadi? ", reply_markup=kelmagan_ishchilar())
        await state.set_state(QuestionsState.kelmagan_ishchilar)
    else:
        await message.answer("Berilgan ma'lumot bo'yicha javob bering iltimos.")
        await message.answer('Ish kunini baholang (1 - 10)', reply_markup=assessment_for_user())
        await state.set_state(QuestionsState.work)


@dp.message(QuestionsState.problem_another_work)
async def set_problem_another_work(message: Message, state: FSMContext):
    if message.text == 'Ortga':
        await message.answer("Ortga", reply_markup=problems_for_user())
        await state.set_state(QuestionsState.problems)
    else:
        await state.update_data({
            "problem_another_work": message.text
        })
        data = await state.get_data()
        if data['status'] == 'False':
            await message.answer("Jamoaning bugungi ishi uchun bahoyingiz", reply_markup=kelmagan_ishchilar())
            await state.set_state(QuestionsState.mark_team)
        elif data['status'] == 'True':
            await message.answer('Yana muammoyingiz bormi? ', reply_markup=yes_not_problem())


@dp.message(QuestionsState.razmer)
async def set_razmer(message: Message, state: FSMContext):
    if message.text == 'Ortga':
        await message.answer("Ortga", reply_markup=problems_for_user())
        await state.set_state(QuestionsState.problems)
    elif message.text == "Shim":
        await state.update_data({
            "razmer": message.text
        })
        await message.answer("Shim uchun qaysi razmer qo'shilishini xohlaysiz?", reply_markup=sizes_of_pants())
        await state.set_state(QuestionsState.razmer_size)
    elif message.text == "Ko'ylak":
        await state.update_data({
            "razmer": message.text
        })
        await message.answer("Ko'ylak uchun qaysi razmer qo'shilishini xohlaysiz?", reply_markup=size_of_dresses())
        await state.set_state(QuestionsState.razmer_size)
    elif message.text == "Ko'fta":
        await state.update_data({
            "razmer": message.text
        })
        await message.answer("Ko'fta uchun qaysi razmer qo'shilishini xohlaysiz?", reply_markup=kofta_sizes())
        await state.set_state(QuestionsState.razmer_size)
    else:
        await message.answer("Berilgan ma'lumot bo'yicha javob bering iltimos.")
        await message.answer("Razmer tanlang", reply_markup=problem_size())
        await state.set_state(QuestionsState.razmer)


@dp.message(QuestionsState.razmer_size)
async def set_razmer_size(message: Message, state: FSMContext):
    if message.text == 'Ortga':
        await message.answer("Ortga", reply_markup=problems_for_user())
        await state.set_state(QuestionsState.problems)
    if message.text == 'Boshqa':
        await message.answer('Boshqa razmer kiriting')
        await state.set_state(QuestionsState.other_size)
    else:
        await state.update_data({
            "razmer_size": message.text
        })
        data = await state.get_data()
        if data['status'] == 'False':
            await message.answer("Jamoaning bugungi ishi uchun bahoyingiz", reply_markup=kelmagan_ishchilar())
            await state.set_state(QuestionsState.mark_team)
        elif data['status'] == 'True':
            await message.answer('Yana muammoyingiz bormi? ', reply_markup=yes_not_problem())


@dp.message(QuestionsState.other_size)
async def set_other_size(message: Message, state: FSMContext):
    await state.update_data({
        "other_size": message.text
    })
    data = await state.get_data()
    if data['status'] == 'False':
        await message.answer("Jamoaning bugungi ishi uchun bahoyingiz", reply_markup=kelmagan_ishchilar())
        await state.set_state(QuestionsState.mark_team)
    elif data['status'] == 'True':
        await message.answer('Yana muammoyingiz bormi? ', reply_markup=yes_not_problem())


@dp.message(QuestionsState.kelmagan_ishchilar)
async def set_kelmagan_ishchilar(message: Message, state: FSMContext):
    await state.update_data({
        "kelmagan_ishchilar": message.text
    })
    data = await state.get_data()
    if data['status'] == 'False':
        await message.answer("Jamoaning bugungi ishi uchun bahoyingiz", reply_markup=kelmagan_ishchilar())
        await state.set_state(QuestionsState.mark_team)
    elif data['status'] == 'True':
        await message.answer('Yana muammoyingiz bormi? ', reply_markup=yes_not_problem())


@dp.message(QuestionsState.mark_team)
async def mark_team(message: Message, state: FSMContext):
    if message.text == 'Ortga':
        await message.answer("Ortga", reply_markup=problems_for_user())
        await state.set_state(QuestionsState.problems)
    else:
        await state.update_data({
            "mark_team": message.text
        })
        data = await state.get_data()
        if data['status'] == 'False':
            await message.answer("Bugun agar nima bo'lganda bundanda yaxshiroq ishlay olar edingiz?")
            await state.set_state(QuestionsState.other_work)
        elif data['status'] == 'True':
            await message.answer('Yana muammoyingiz bormi? ', reply_markup=yes_not_problem())


@dp.message(QuestionsState.other_work)
async def set_other_work(message: Message, state: FSMContext):
    await state.update_data({"other_work": message.text})

    await message.answer('Yana muammoyingiz bormi? ', reply_markup=yes_not_problem())


@dp.callback_query(lambda callback_data: callback_data.data == 'yes')
async def set_problem(callback_data: CallbackQuery, state: FSMContext):
    await callback_data.message.delete()
    await state.update_data({
        'status': 'True'
    })
    await callback_data.message.answer("Bor", reply_markup=problems_for_user())
    await state.set_state(QuestionsState.problems)


@dp.callback_query(lambda callback_data: callback_data.data == "no")
async def get_all_data(callback_data: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    finally_data = {}

    user_chat_id = callback_data.message.chat.id
    user_name = get_user_name(user_chat_id)
    returning_message = f"👤 {user_name}ning {datetime.today().date()} kungi hisoboti:\n"

    fields = {
        'work': 'Bugungi ish baholandi',
        'problems': 'Ish kunidagi muammo',
        'problem_another_work': 'Aynan qanday muammo',
        'razmer': 'Shu kiyim da yetarli razmer mavjud emas',
        'razmer_size': 'Aynan qaysi razmer(lar)',
        'other_size': 'Aynan qaysi razmer(lar)',
        'kelmagan_ishchilar': 'Bugun ishga kelmaganlar soni',
        'mark_team': 'Bugungi jamoaning ishi baholandi',
        'other_work': 'Bugun agar nima bo\'lganda bundanda yaxshiroq ishlay olishi'
    }

    for key, description in fields.items():
        if data.get(key) is not None:
            finally_data[key] = data[key]
            returning_message += f"\n- {description}: {data[key]}"
    finally_data['user_chat_id'] = user_chat_id
    insert_data_to_base(finally_data)

    await callback_data.message.answer(f"Bugungi Hisobot ni topshirganingiz uchun rahmat, {user_name}.")

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': ADMIN_CHAT_ID,
        'text': returning_message
    }
    requests.post(url, json=payload)

    return True


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
