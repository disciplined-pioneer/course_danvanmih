from db.models.models import Doctors, Schedules

# Удаление всей информации о врача по его id
async def delete_info_doctor(doctor_id: int):

    doctor_info = await Doctors.get(id_doctor=doctor_id)
    schedules_info = await Schedules.get(doctor_id=doctor_id)
    if doctor_info:
        name_doctor = doctor_info.full_name
        await doctor_info.delete()
        if schedules_info:
            await schedules_info.delete()
    else:
        return 'неизвестно', False
    return name_doctor, True