from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_or_cancel_btn():
    confirm_btn = InlineKeyboardButton(text='Confirm ✅', callback_data='confirm')
    cancel_btn = InlineKeyboardButton(text='Cancel ❌ ', callback_data='cancel')
    finally_btn_data = InlineKeyboardMarkup(inline_keyboard=[[confirm_btn], [cancel_btn]])
    return finally_btn_data


def assessment_work_day():
    one = InlineKeyboardButton(text='1', callback_data='1')
    two = InlineKeyboardButton(text='2', callback_data='2')
    three = InlineKeyboardButton(text='3', callback_data='3')
    four = InlineKeyboardButton(text='4', callback_data='4')
    five = InlineKeyboardButton(text='5', callback_data='5')
    six = InlineKeyboardButton(text='6', callback_data='6')
    seven = InlineKeyboardButton(text='7', callback_data='7')
    eight = InlineKeyboardButton(text='8', callback_data='8')
    nine = InlineKeyboardButton(text='9', callback_data='9')
    ten = InlineKeyboardButton(text='10', callback_data='10')
    finally_btn_data = InlineKeyboardMarkup(
        inline_keyboard=[[one, two, three], [four, five, six], [seven, eight, nine], [ten]])
    return finally_btn_data