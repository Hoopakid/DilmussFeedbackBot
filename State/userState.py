from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    name = State()
    branch = State()
    time = State()
    team = State()


class QuestionsState(StatesGroup):
    work = State()
