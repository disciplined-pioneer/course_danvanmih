from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models.models import Specializations, Doctors

PATIENT_FIELDS = {
    "full_name": {"label": "ФИО", "type": "text"},
    "address": {"label": "Адрес", "type": "text"},
    "birth_date": {"label": "Дата рождения", "type": "text"},
    "phone": {"label": "Телефон", "type": "text"},
}

async def patient_edit_keyb(patient_id: int):
    fields = build_edit_fields_keyboard(
        patient_id,
        PATIENT_FIELDS,
        "edit_patient"
    )

    return InlineKeyboardMarkup(inline_keyboard=fields)

DOCTOR_FIELDS = {
    "full_name": {
        "label": "ФИО",
        "type": "text"
    },
    "cabinet": {
        "label": "Кабинет",
        "type": "text"
    },
    "specialization_id": {
        "label": "Специализация",
        "type": "select",
        "options_source": "specializations"
    },
}

SCHEDULE_FIELDS = {
    "day_of_week": {
        "label": "День недели",
        "type": "select",
        "options_source": "weekdays"
    },
    "start_time": {
        "label": "Начало",
        "type": "time"
    },
    "end_time": {
        "label": "Конец",
        "type": "time"
    },
}

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


def build_edit_fields_keyboard(obj_id: int, fields: dict, prefix: str):
    return [
        [
            InlineKeyboardButton(
                text=v["label"],
                callback_data=f"{prefix}:{obj_id}:{k}"
            )
        ]
        for k, v in fields.items()
    ]

async def doctor_edit_keyb(doctor_id: int):
    fields = build_edit_fields_keyboard(
        doctor_id,
        DOCTOR_FIELDS,
        "edit_doctor"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="❌ Удалить врача",
                callback_data=f"delete_doctor:{doctor_id}"
            )]
        ]
        + fields
        + [
            [InlineKeyboardButton(
                text="🔙 К списку врачей",
                callback_data="doctor_search"
            )]
        ]
    )

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
