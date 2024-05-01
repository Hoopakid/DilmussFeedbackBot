from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from Database.datas import get_branch_datas, get_team_data


def choose_time_btn():
    kechki = KeyboardButton(text='Kechki 🌃')
    kunduzgi = KeyboardButton(text='Kunduzgi 🏙')
    finally_btn = ReplyKeyboardMarkup(keyboard=[[kechki], [kunduzgi]], resize_keyboard=True, one_time_keyboard=True)
    return finally_btn


def branch_btn():
    branches = get_branch_datas()
    buttons = []
    for branch in branches:
        buttons.append([KeyboardButton(text=branch.get('branch'))])
    finally_btn = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    return finally_btn


def choose_team_btn(branch_id: int):
    teams = get_team_data(branch_id)
    buttons = []
    for team in teams:
        buttons.append([KeyboardButton(text=team.get('team_name'))])
    finally_btn = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    return finally_btn


def edit_user_data_btn():
    name = KeyboardButton(text="Ism")
    branch = KeyboardButton(text="Filial")
    time = KeyboardButton(text="Vaqt")
    finally_btn = ReplyKeyboardMarkup(keyboard=[[name, time], [branch]], resize_keyboard=True, one_time_keyboard=True)
    return finally_btn
