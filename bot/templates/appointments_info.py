from db.models.models import Appointments, Patients
from datetime import datetime

async def build_appointment_text(appointment_id: int):
    appt = await Appointments.get(id_appointment=appointment_id)

    patient = await Patients.get(id_patient=appt.patient_id)

    dt = datetime.combine(appt.appointment_date, appt.appointment_time)

    text = (
        f"🩺 Приём №{appt.id_appointment}\n\n"

        f"👤 Пациент: {patient.full_name}\n"
        f"🏠 Адрес: {patient.address}\n"
        f"🎂 Дата рождения: "
        f"{patient.birth_date.strftime('%d.%m.%Y') if patient.birth_date else 'Не указана'}\n"
        f"📞 Телефон: {patient.phone or 'Не указан'}\n\n"

        f"📅 Дата и время: {dt.strftime('%d.%m.%Y %H:%M')}\n"
        f"📝 Диагноз: {appt.diagnosis or 'Не указан'}\n"
        f"📌 Решение: {appt.decision or 'Не указано'}\n"
    )

    return text