from celery import Celery
from celery.schedules import crontab
import asyncio
from datetime import datetime

from Database.datas import get_all_user_chat_ids, get_user_time
from Keyboards.InlineKeyboards import start_questions
from main import bot

app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

app.conf.beat_schedule = {
    'check_and_send_messages': {
        'task': 'tasks.check_and_send_messages',
        'schedule': crontab(minute='*')
    }
}
app.conf.timezone = 'UTC'


async def send_message_if_needed(user_chat_id):
    now = datetime.utcnow()
    user_time = get_user_time(user_chat_id['user_chat_id'])
    if user_time == 1 and now.hour == 12 and now.minute == 30:
        await bot.send_message(user_chat_id['user_chat_id'], 'Ish kunini baholang', reply_markup=start_questions())
    elif user_time == 2 and now.hour == 18 and now.minute == 30:
        await bot.send_message(user_chat_id['user_chat_id'], 'Ish kunini baholang', reply_markup=start_questions())


def send_async_messages(user_chat_ids):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def send_messages_concurrently():
        tasks = [send_message_if_needed(user) for user in user_chat_ids]
        await asyncio.gather(*tasks)
        return "Success"

    return loop.run_until_complete(send_messages_concurrently())


@app.task
def check_and_send_messages():
    user_chat_ids = get_all_user_chat_ids()
    send_async_messages(user_chat_ids)
