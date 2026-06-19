import re
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from core.bot import bot

class DiagnosisStates(StatesGroup):
    new_diagnosis = State()

class PatientCreateStates(StatesGroup):
    full_name = State()
    address = State()
    birth_date = State()
    phone = State()
    confirm = State()

def parse_date(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except:
        return None


def parse_phone(value: str):
    # очень простая проверка (не усложняй без нужды)
    if re.match(r"^\+?\d{10,15}$", value):
        return value
    return None

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
