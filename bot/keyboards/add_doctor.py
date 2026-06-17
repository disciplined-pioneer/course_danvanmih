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

back_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]
    ]
)