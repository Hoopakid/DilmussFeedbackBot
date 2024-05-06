from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from Database.datas import get_branch_datas, get_team_data


def choose_time_btn():
    kunduzgi = KeyboardButton(text='Kunduzgi 🏙')
    kechki = KeyboardButton(text='Kechki 🌃')
    finally_btn = ReplyKeyboardMarkup(keyboard=[[kunduzgi], [kechki]], resize_keyboard=True, one_time_keyboard=True)
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


def assessment_for_user():
    one = KeyboardButton(text="1")
    two = KeyboardButton(text="2")
    three = KeyboardButton(text="3")
    four = KeyboardButton(text="4")
    five = KeyboardButton(text="5")
    six = KeyboardButton(text="6")
    seven = KeyboardButton(text="7")
    eight = KeyboardButton(text="8")
    nine = KeyboardButton(text="9")
    ten = KeyboardButton(text="10")
    finally_btn = ReplyKeyboardMarkup(keyboard=[[one, two, three, four], [five, six, seven, eight], [nine, ten]],
                                      resize_keyboard=True, one_time_keyboard=True)
    return finally_btn


def problems_for_user():
    other_work = KeyboardButton(text="Boshqa ishga fokus bo'lishi")
    not_size = KeyboardButton(text="Razmer yo'q")
    team = KeyboardButton(text="Jamoa a'zolari kelmadi")
    finally_btn = ReplyKeyboardMarkup(keyboard=[[other_work], [not_size], [team]], resize_keyboard=True,
                                      one_time_keyboard=True)
    return finally_btn


def problem_other():
    razdevalka = KeyboardButton(text="Razdevalka bilan")
    open_product = KeyboardButton(text="Tovar ochish bilan")
    security = KeyboardButton(text="Xavfsizlik xodimi bilan")
    to_street = KeyboardButton(text="Ko'chaga aksiyaga")
    back = KeyboardButton(text="Ortga")
    finally_btn = ReplyKeyboardMarkup(keyboard=[[razdevalka], [open_product], [security], [to_street], [back]])
    return finally_btn


def problem_size():
    koylak = KeyboardButton(text="Shim")
    shim = KeyboardButton(text="Ko'ylak")
    kofta = KeyboardButton(text="Ko'fta")
    back = KeyboardButton(text="Ortga")
    finally_btn = ReplyKeyboardMarkup(keyboard=[[koylak, shim], [kofta, back]], resize_keyboard=True,
                                      one_time_keyboard=True)
    return finally_btn


def sizes_of_pants():
    x = KeyboardButton(text="X")
    xl = KeyboardButton(text="XL")
    s = KeyboardButton(text="S")
    m = KeyboardButton(text="M")
    l = KeyboardButton(text="L")
    two_xl = KeyboardButton(text="2XL")
    three_xl = KeyboardButton(text="3XL")
    other = KeyboardButton(text="Boshqa")
    back = KeyboardButton(text="Ortga")
    finally_btn = ReplyKeyboardMarkup(keyboard=[[x, xl, s], [m, l, two_xl], [three_xl, other], [back]],
                                      resizer_keyboard=True,
                                      one_time_keyboard=True)
    return finally_btn


def size_of_dresses():
    ottiz_sakkiz = KeyboardButton(text="38")
    ottiz_toqqiz = KeyboardButton(text="39")
    qirq = KeyboardButton(text="40")
    qirq_bir = KeyboardButton(text="41")
    qirq_ikki = KeyboardButton(text="42")
    qirq_uch = KeyboardButton(text="43")
    qirq_tort = KeyboardButton(text="44")
    qirq_besh = KeyboardButton(text="45")
    qirq_olti = KeyboardButton(text="46")
    qirq_yetti = KeyboardButton(text="47")
    qirq_sakkiz = KeyboardButton(text="48")
    qirq_toqqiz = KeyboardButton(text="49")
    ellik = KeyboardButton(text="50")
    ellik_bir = KeyboardButton(text="51")
    other = KeyboardButton(text="Boshqa")
    back = KeyboardButton(text="Ortga")
    finally_btn_data = ReplyKeyboardMarkup(
        keyboard=[[ottiz_sakkiz, ottiz_toqqiz, qirq], [qirq_bir, qirq_ikki, qirq_uch],
                  [qirq_tort, qirq_besh, qirq_olti], [qirq_yetti, qirq_sakkiz, qirq_toqqiz],
                  [ellik, ellik_bir, other], [back]
                  ], resize_keyboard=True, one_time_keyboard=True)
    return finally_btn_data


def kofta_sizes():
    xs = KeyboardButton(text='XS')
    s = KeyboardButton(text='S')
    m = KeyboardButton(text='M')
    l = KeyboardButton(text='L')
    xl = KeyboardButton(text='XL')
    xxl = KeyboardButton(text='XXL')
    other = KeyboardButton(text='Boshqa')
    back = KeyboardButton(text='Ortga')
    finally_btn_data = ReplyKeyboardMarkup(
        keyboard=[[xs, s, m], [l, xl, xxl], [other, back]], resize_keyboard=True, one_time_keyboard=True
    )
    return finally_btn_data


def kelmagan_ishchilar():
    one = KeyboardButton(text="1")
    two = KeyboardButton(text="2")
    three = KeyboardButton(text="3")
    four = KeyboardButton(text="4")
    five = KeyboardButton(text="5")
    back = KeyboardButton(text="Ortga")
    finally_btn_data = ReplyKeyboardMarkup(
        keyboard=[[one, two, three], [four, five], [back]], resize_keyboard=True, one_time_keyboard=True
    )
    return finally_btn_data
