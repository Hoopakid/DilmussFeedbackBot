from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_or_cancel_btn():
    confirm_btn = InlineKeyboardButton(text='Confirm ✅', callback_data='confirm')
    cancel_btn = InlineKeyboardButton(text='Cancel ❌ ', callback_data='cancel')
    finally_btn_data = InlineKeyboardMarkup(inline_keyboard=[[confirm_btn], [cancel_btn]])
    return finally_btn_data
