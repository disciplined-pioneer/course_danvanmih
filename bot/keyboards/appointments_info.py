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

async def get_doctor_appointments(doctor_id: int):
    appointments=await Appointments.filter(doctor_id=doctor_id)

    if not appointments:
        return "❕ У врача нет приёмов",None

    text="📅 Приёмы врача:\n\n"

    keyboard=InlineKeyboardMarkup(inline_keyboard=[
        *[[InlineKeyboardButton(
            text=f"Приём №{app.id_appointment} ({app.appointment_date})",
            callback_data=f"app_id_info:{app.id_appointment}"
        )]for app in appointments],
        [InlineKeyboardButton(text="◀️ Назад",callback_data="appointments_info")]
    ])

    return text,keyboard

async def doctor_appointment_actions_kb(doctor_id: int):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✏️ Изменить диагноз', callback_data=f'change_diagnosis')],
            [InlineKeyboardButton(text='❌ Удалить приём', callback_data=f'delete_appointment')],
            [InlineKeyboardButton(text='◀️ К списку приёмов', callback_data=f'doctor_id_appts:{doctor_id}')]
        ]
    )
    return keyb


back_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='◀️ Назад', callback_data='appointments_info')]
    ]
)
