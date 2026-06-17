from db.models.models import Doctors


# Текст для вывода карточки врача по его id
async def build_doctor_card(doctor_id: int) -> str:
    
    doctor = await Doctors.get(id_doctor=doctor_id)

    if not doctor:
        return "❌ Врач не найден"

    if doctor.schedules:
        schedule_text = ", ".join(
            f"{s.day_of_week} {s.start_time:%H:%M}-{s.end_time:%H:%M}"
            for s in doctor.schedules
        )
    else:
        schedule_text = "нет расписания"

    return (
        f"👨‍⚕️ Карточка врача\n"
        f"ФИО: {doctor.full_name}\n"
        f"Специализация: {doctor.specialization.name if doctor.specialization else '—'}\n"
        f"Кабинет: {doctor.cabinet or '—'}\n"
        f"График работы: {schedule_text}"
    )