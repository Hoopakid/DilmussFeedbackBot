from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    name = State()
    branch = State()
    time = State()
    team = State()


class QuestionsState(StatesGroup):
    work = State()
    problems = State()
    problem_another_work = State()
    razmer = State()
    razmer_size = State()
    other_size = State()
    kelmagan_ishchilar = State()
    mark_team = State()
    other_work = State()
