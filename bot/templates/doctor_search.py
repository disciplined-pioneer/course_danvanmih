from db.models.models import Doctors, Schedules, Specializations


# Текст для вывода карточки врача по его id
async def build_doctor_card(doctor_id: int) -> str:

    doctor = await Doctors.get(id_doctor=doctor_id)

    if not doctor:
        return "❌ Врач не найден"

    # расписание — ВСЕ записи
    schedules = await Schedules.filter(doctor_id=doctor_id)

    if schedules:
        schedule_text = ", ".join(
            f"{s.day_of_week} {s.start_time:%H:%M}-{s.end_time:%H:%M}"
            for s in schedules
        )
    else:
        schedule_text = "нет расписания"

    # специализация — ОДНА запись
    spec = await Specializations.get(id_specialization=doctor.specialization_id)

    spec_name = spec.name if spec else "—"

    return (
        "👨‍⚕️ Карточка врача\n"
        f"ФИО: {doctor.full_name}\n"
        f"Специализация: {spec_name}\n"
        f"Кабинет: {doctor.cabinet or '—'}\n"
        f"График работы: {schedule_text}"
    )

def doctor_deleted_message(name_doctor: str) -> str:
    return f'✅ Доктор "{name_doctor}" был успешно удалён'

doctor_delete_error = "❌ Ошибка удаления доктора"

new_cabinet_text = 'Введите новый номер кабинета'

new_doctor_cabinet = 'Кабинет доктора был изменён'