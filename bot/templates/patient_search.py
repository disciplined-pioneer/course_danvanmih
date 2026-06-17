from db.models.models import Patients
from aiogram.fsm.state import StatesGroup, State

class AppointmentStates(StatesGroup):
    datetime = State()


# Текст для вывода карточки врача по его id
async def build_patient_card(patient_id: int) -> str:

    patient = await Patients.get(id_patient=patient_id)

    if not patient:
        return "❌ пациент не найден"

    return (
        "👤 Карточка пациента\n"
        f"ФИО: {patient.full_name}\n"
        f"Адрес: {patient.address}\n"
        f"Дата рождения: {patient.birth_date}\n"
        f"Телефон: {patient.phone}"
    )

def patient_deleted_message(name_patient: str) -> str:
    return f'✅ Пациент "{name_patient}" был успешно удалён'

patient_delete_error = "❌ Ошибка удаления пациента"

error_datetime_format = "❌ Формат: YYYY-MM-DD HH:MM"

appointment_created = "✅ Приём создан"

enter_datetime = "Введите дату и время:\nФормат: YYYY-MM-DD HH:MM"