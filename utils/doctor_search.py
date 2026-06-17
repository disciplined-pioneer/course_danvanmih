from db.models.models import Doctors

# Удаление всей информации о врача по его id
async def delete_info_doctor(doctor_id: int):
    return 'Крутой доктор', True