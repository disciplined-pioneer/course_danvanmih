from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_admin_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="start_menu_admin")]
    ]
)

start_user_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👨‍⚕️ Поиск врача", callback_data="doctor_search")],
        [InlineKeyboardButton(text="👤 Поиск пациента", callback_data="patient_search")],
        [InlineKeyboardButton(text="🗓 Расписание врачей", callback_data="doctor_schedule")],
        [InlineKeyboardButton(text="📋 Сведения о приёмах", callback_data="appointments_info")]
    ]
)