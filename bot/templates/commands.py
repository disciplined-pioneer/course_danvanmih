from db.models.models import Schedules, Specializations

async def format_doctor_card(doctor) -> str:

    schedules = await Schedules.filter(doctor_id=doctor.id_doctor)
    if schedules:
        schedule_text = ", ".join(
            f"{s.day_of_week} {s.start_time:%H:%M}-{s.end_time:%H:%M}"
            for s in schedules
        )
    else:
        schedule_text = "нет расписания"
    spec = await Specializations.get(id_specialization=doctor.specialization_id)

    spec_name = spec.name if spec else "—"
    return (
        "👨‍⚕️ Карточка врача\n"
        f"ФИО: {doctor.full_name}\n"
        f"Специализация: {spec_name}\n"
        f"Кабинет: {doctor.cabinet or '—'}\n"
        f"График работы: {schedule_text}"
    )

async def format_patient_card(patient) -> str:
    return (
        "👤 Карточка пациента\n"
        f"ФИО: {patient.full_name}\n"
        f"Адрес: {patient.address}\n"
        f"Дата рождения: {patient.birth_date}\n"
        f"Телефон: {patient.phone}"
    )