from celery import Celery
from celery.schedules import crontab
from aiogram.exceptions import AiogramError
import asyncio
import logging

from Database.datas import get_all_user_chat_ids, get_user_time
from Keyboards.InlineKeyboards import start_questions
from main import bot

app = Celery(
    'tasks',
    broker='redis://redis_dilmuss:6379/0',
    backend='redis://redis_dilmuss:6379/0'
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Schedule the tasks to run at 12:30 and 18:30
app.conf.beat_schedule = {
    'check_and_send_messages_first': {
        'task': 'tasks.check_and_send_messages_first',
        'schedule': crontab(hour=12, minute=30)
    },
    'check_and_send_messages_second': {
        'task': 'tasks.check_and_send_messages_second',
        'schedule': crontab(hour=18, minute=30)
    }
}
app.conf.timezone = 'UTC'


async def send_message_if_needed(user_chat_id, expected_user_time):
    try:
        user_time = get_user_time(user_chat_id['user_chat_id'])
        if user_time == expected_user_time:
            await bot.send_message(user_chat_id['user_chat_id'], 'Ish kunini baholashni boshlaymizmi 😉',
                                   reply_markup=start_questions())
    except AiogramError as e:
        logger.error(f"Failed to send message to user {user_chat_id['user_chat_id']}")


def send_async_messages(user_chat_ids, expected_user_time):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def send_messages_concurrently():
        tasks = [send_message_if_needed(user, expected_user_time) for user in user_chat_ids]
        await asyncio.gather(*tasks)
        return "Success"

    return loop.run_until_complete(send_messages_concurrently())


@app.task
def check_and_send_messages_first():
    user_chat_ids = get_all_user_chat_ids()
    send_async_messages(user_chat_ids, expected_user_time=1)


@app.task
def check_and_send_messages_second():
    user_chat_ids = get_all_user_chat_ids()
    send_async_messages(user_chat_ids, expected_user_time=2)
