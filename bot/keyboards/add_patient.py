from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def confirm_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="patient:yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="patient:no"),
            ]
        ]
    )