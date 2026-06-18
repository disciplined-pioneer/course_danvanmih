from db.models.models import Patients
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from core.bot import bot

class AppointmentStates(StatesGroup):
    datetime = State()
    new_address = State()

# Удаление всей информации о врача по его id
async def delete_info_patient(patient_id: int):

    patient_info = await Patients.get(id_patient=patient_id)
    if patient_info:
        name_patient = patient_info.full_name
        await patient_info.delete()
    else:
        return 'неизвестно', False
    return name_patient, True

async def safe_edit(state: FSMContext, chat_id: int, text: str, kb=None):

    try:
        data = await state.get_data()
        last_id = data.get("last_id_message")

        if not last_id:
            msg = await bot.send_message(chat_id, text, reply_markup=kb)
            await state.update_data(last_id_message=msg.message_id)
            return msg

        msg = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=last_id,
            text=text,
            reply_markup=kb
        )

        await state.update_data(last_id_message=msg.message_id)
    except:
        return last_id
    return msg
