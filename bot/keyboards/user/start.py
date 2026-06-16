from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_admin_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="привет", callback_data="hello")]
    ]
)

back_admin_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="start_menu_admin")]
    ]
)

start_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="привет", callback_data="hello")]
    ]
)