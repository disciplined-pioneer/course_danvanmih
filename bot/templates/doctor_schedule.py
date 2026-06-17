from db.models.models import Schedules, Doctors, Specializations

# Выводим расписание врачей конкретной специальности
async def list_doctors_spec(spec_id: int):

    spec_info = await Specializations.get(id_specialization=spec_id)
    doctors = await Doctors.filter(specialization_id=spec_id)
    lines = [f'📋 Расписание по специализации: "{spec_info.name}"']
    for d in doctors:
        schedules = await Schedules.filter(doctor_id=d.id_doctor)
        if schedules:
            lines.append(
                f"👨‍⚕️ {d.full_name} (Кабинет {d.cabinet or '—'}) — " +
                ", ".join(f"{s.day_of_week}: {s.start_time:%H:%M}-{s.end_time:%H:%M}" for s in schedules)
            )
    return "\n".join(lines)