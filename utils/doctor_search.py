from db.models.models import Doctors, Schedules
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from core.bot import bot

class DoctorInfoStates(StatesGroup):
    new_cabinet = State()

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
