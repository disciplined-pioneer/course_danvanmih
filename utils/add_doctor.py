import re
from datetime import time
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from core.bot import bot

class DoctorCreateStates(StatesGroup):
    full_name = State()
    specialization_id = State()
    cabinet = State()
    day_of_week = State()
    start_time = State()
    end_time = State()
    confirm = State()


def parse_time(value: str):
    if not re.match(r"^\d{2}:\d{2}$", value):
        return None

    try:
        h, m = map(int, value.split(":"))
        if 0 <= h < 24 and 0 <= m < 60:
            return time(hour=h, minute=m)
    except:
        return None

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


async def go_back(state: FSMContext, chat_id: int, step_text: str):
    data = await state.get_data()

    history = data.get("history", [])
    if not history:
        await safe_edit(state, chat_id, "Вы на первом шаге")
        return None

    history.pop()
    await state.update_data(history=history)

    await safe_edit(state, chat_id, step_text)
    return True