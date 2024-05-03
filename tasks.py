from Database.datas import get_all_user_chat_ids
from State.userState import QuestionsState
from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0'
)


@app.task
def send_message_to_all_users():
    async def send_question():
        user_chat_ids = get_all_user_chat_ids()
