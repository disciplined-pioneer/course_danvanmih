from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models.models import Patients


# Вывод всех врачей + текст
async def buttons_with_all_patients():
    patients = await Patients.all()

    if not patients:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]]
        ), '❕ Пока нет доступных пациентов'

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=d.full_name, callback_data=f'patient_id:{d.id_patient}')]
            for d in patients
        ] + [[InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]]
    ), 'Выберите пациента'

# Удаление пациента + список пациентов
async def patient_delete_keyb(patient_id: int):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Удалить пациента", callback_data=f"delete_patient:{patient_id}")],
            [InlineKeyboardButton(text="🔙 К списку пациентов", callback_data="patient_search")]
        ]
    )
    return keyb


back_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]
    ]
)
