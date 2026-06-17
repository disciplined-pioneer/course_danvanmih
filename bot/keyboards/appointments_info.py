from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models.models import Doctors, Appointments

# Вывод всех врачей + текст
async def doctors_appts_kb():

    appointments = await Appointments.all()
    doctor_ids = list({app.doctor_id for app in appointments})

    if not doctor_ids:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]]
        ), '❕ Пока нет доступных приёмов'

    all_doctors = await Doctors.all()
    doctors = [d for d in all_doctors if d.id_doctor in doctor_ids]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=d.full_name, callback_data=f'doctor_id_appts:{d.id_doctor}')]
            for d in doctors
        ] + [
            [InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]
        ]
    ), 'Выберите врача'

back_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]
    ]
)
