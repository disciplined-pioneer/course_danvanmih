from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models.models import Specializations, Doctors


# Вывод всех врачей + текст
async def buttons_with_all_doctors():
    doctors = await Doctors.all()

    if not doctors:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]]
        ), '❕ Пока нет доступных врачей'

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=d.full_name, callback_data=f'doctor_id:{d.id_doctor}')]
            for d in doctors
        ] + [[InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]]
    ), 'Выберите врача'


back_list_doctors = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 К списку врачей", callback_data="doctor_search")]
    ]
)
