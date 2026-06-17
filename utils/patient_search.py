from db.models.models import Patients

# Удаление всей информации о врача по его id
async def delete_info_patient(patient_id: int):

    patient_info = await Patients.get(id_patient=patient_id)
    if patient_info:
        name_patient = patient_info.full_name
        await patient_info.delete()
    else:
        return 'неизвестно', False
    return name_patient, True