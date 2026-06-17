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

def back_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад", callback_data="patient:back")]
        ]
    )

back_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='◀️ Назад', callback_data='patient_search')]
    ]
)