from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models.models import Patients, Doctors


# Вывод всех врачей + текст
async def buttons_with_all_patients():
    patients = await Patients.all()

    if not patients:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='➕ Добавить пациента', callback_data='add_patient')],
                [InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]
            ]
        ), '❕ Пока нет доступных пациентов'

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='➕ Добавить пациента', callback_data='add_patient')]
        ] + [
            [InlineKeyboardButton(text=d.full_name, callback_data=f'patient_id:{d.id_patient}')]
            for d in patients
        ] + [
            [InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]
        ]
    ), 'Выберите пациента'

# Удаление пациента + список пациентов
async def patient_delete_keyb(patient_id: int):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Удалить пациента", callback_data=f"delete_patient:{patient_id:}")],
            [InlineKeyboardButton(text="✏️ Изменить адрес", callback_data=f"change_address:{patient_id:}")],
            [InlineKeyboardButton(text="➕ Добавить приём", callback_data=f"add_appointment:{patient_id:}")],
            [InlineKeyboardButton(text="🔙 К списку пациентов", callback_data="patient_search")]
        ]
    )
    return keyb

async def buttons_with_all_doctors(patient_id:int):
    doctors=await Doctors.all()

    if not doctors:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔙 Меню',callback_data='back_start_menu')]]),'❕ Пока нет доступных врачей'

    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=d.full_name,callback_data=f'doctor_id_appointment:{d.id_doctor}')] for d in doctors]+[
            [InlineKeyboardButton(text='🔙 Назад',callback_data=f'patient_id:{patient_id}')]
        ]
    ),'Выберите врача для записи на приём'

async def info_patient_keyb(patient_id:int):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔙 Назад', callback_data=f'patient_id:{patient_id}')]
        ]
    )
    return keyb

back_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]
    ]
)

back_doctor_list_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Назад', callback_data='add_appointment')]
    ]
)

