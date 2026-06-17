from db.models.models import Specializations
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
        [InlineKeyboardButton(text='◀️ Назад', callback_data='doctor_search')]
    ]
)

# Вывод всех специализаций + текст
async def buttons_with_all_specializations():
    specs = await Specializations.all()

    keyboard = (
        [[InlineKeyboardButton(text="➕ Добавить новую специализацию", callback_data="add_spec")]] +
        ([[InlineKeyboardButton(text=s.name, callback_data=f"spec_id:{s.id_specialization}")] for s in specs]
         if specs else []) +
        [[InlineKeyboardButton(text="⬅ Назад", callback_data="doc:back")]]
    )

    text = "Выберите специализацию врача" if specs else "❕ Пока нет доступных специализаций"

    return InlineKeyboardMarkup(inline_keyboard=keyboard), text