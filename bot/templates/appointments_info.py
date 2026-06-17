from db.models.models import Appointments, Patients
from datetime import datetime

async def build_doctor_appointments_text(doctor_id: int):
    appointments = await Appointments.filter(doctor_id=doctor_id)

    if not appointments:
        return "❕ У врача нет приёмов"

    text = "📅 Приёмы врача:\n\n"

    for appt in appointments:
        patient = await Patients.get(id_patient=appt.patient_id)

        dt = datetime.combine(appt.appointment_date, appt.appointment_time)

        text += (
            f"🩺 Приём #{appt.id_appointment}\n"
            f"👤 Пациент: {patient.full_name}\n"
            f"📅 {dt.strftime('%Y-%m-%d %H:%M')}\n"
            f"📌 Статус: {appt.decision}\n"
            "──────────────\n"
        )

    return text