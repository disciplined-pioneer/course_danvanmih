from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models.models import Specializations, Doctors

async def buttons_with_all_doctors():
    doctors = await Doctors.all()

    if not doctors:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='📝 Добавить врача', callback_data='add_doctor')],
                [InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]
            ]
        ), '❕ Пока нет доступных врачей'

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='📝 Добавить врача', callback_data='add_doctor')]
        ] + [
            [InlineKeyboardButton(text=d.full_name, callback_data=f'doctor_id:{d.id_doctor}')]
            for d in doctors
        ] + [
            [InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]
        ]
    ), 'Выберите врача'

# Удаление врача + список врачей
async def doctor_edit_keyb(doctor_id: int):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ ФИО", callback_data=f"edit_doctor:{doctor_id}:full_name")],
            [InlineKeyboardButton(text="✏️ Кабинет", callback_data=f"edit_doctor:{doctor_id}:cabinet")],
            [InlineKeyboardButton(text="✏️ Телефон", callback_data=f"edit_doctor:{doctor_id}:phone")],
            [InlineKeyboardButton(text="✏️ Специализация", callback_data=f"edit_doctor:{doctor_id}:specialization")],
            [InlineKeyboardButton(text="❌ Удалить врача", callback_data=f"delete_doctor:{doctor_id}")],
            [InlineKeyboardButton(text="🔙 К списку врачей", callback_data="doctor_search")]
        ]
    )
    return keyb

async def info_doctor_keyb(doctor_id:int):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔙 Назад', callback_data=f'doctor_id:{doctor_id}')]
        ]
    )
    return keyb

back_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]
    ]
)
