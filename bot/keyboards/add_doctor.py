from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def back_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад", callback_data="doc:back")]
        ]
    )


def confirm_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="doc:yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="doc:no"),
            ]
        ]
    )