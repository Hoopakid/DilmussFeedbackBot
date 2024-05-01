from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


def get_dispatcher():
    return Dispatcher(storage=MemoryStorage())
