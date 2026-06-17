from aiogram import Router, F, types, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from core.bot import bot

import re
from datetime import time

router = Router()


# =========================
# FSM
# =========================

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

# =========================
# KEYBOARDS
# =========================

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад", callback_data="doc:back")]
        ]
    )


def confirm_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="doc:yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="doc:no"),
            ]
        ]
    )


# =========================
# SAFE EDIT
# =========================

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


# =========================
# START
# =========================

@router.callback_query(F.data == "add_doctor")
async def start(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(history=[])

    msg = await call.message.edit_text("Введите ФИО врача:")

    await state.set_state(DoctorCreateStates.full_name)
    await state.update_data(last_id_message=msg.message_id)


# =========================
# BACK LOGIC
# =========================

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


# =========================
# FULL NAME
# =========================

@router.message(DoctorCreateStates.full_name)
async def full_name(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        return await go_back(state, message.from_user.id, "Введите ФИО врача:")

    await state.update_data(full_name=message.text)
    await message.delete()

    data = await state.get_data()
    data["history"].append("full_name")
    await state.update_data(history=data["history"])

    await state.set_state(DoctorCreateStates.specialization_id)

    await safe_edit(state, message.from_user.id, "Введите ID специализации:", back_kb())


# =========================
# SPECIALIZATION
# =========================

@router.message(DoctorCreateStates.specialization_id)
async def spec(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        return await go_back(state, message.from_user.id, "Введите ФИО врача:")

    if not message.text.isdigit():
        await safe_edit(state, message.from_user.id, "❌ ID должен быть числом", back_kb())
        return

    await state.update_data(specialization_id=int(message.text))
    await message.delete()

    data = await state.get_data()
    data["history"].append("spec")
    await state.update_data(history=data["history"])

    await state.set_state(DoctorCreateStates.cabinet)

    await safe_edit(state, message.from_user.id, "Введите кабинет (или '-'):", back_kb())


# =========================
# CABINET
# =========================

@router.message(DoctorCreateStates.cabinet)
async def cabinet(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        return await go_back(state, message.from_user.id, "Введите ID специализации:")

    await state.update_data(cabinet=None if message.text == "-" else message.text)
    await message.delete()

    data = await state.get_data()
    data["history"].append("cabinet")
    await state.update_data(history=data["history"])

    await state.set_state(DoctorCreateStates.day_of_week)

    await safe_edit(state, message.from_user.id, "Введите день недели:", back_kb())


# =========================
# DAY
# =========================

@router.message(DoctorCreateStates.day_of_week)
async def day(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        return await go_back(state, message.from_user.id, "Введите кабинет:")

    await state.update_data(day_of_week=message.text)
    await message.delete()

    await state.set_state(DoctorCreateStates.start_time)

    await safe_edit(state, message.from_user.id, "Введите время начала:", back_kb())


# =========================
# START TIME
# =========================

@router.message(DoctorCreateStates.start_time)
async def start_time(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        return await go_back(state, message.from_user.id, "Введите день недели:")

    parsed = parse_time(message.text)

    if not parsed:
        await safe_edit(state, message.from_user.id, "❌ Время должно быть в формате HH:MM (00:00–23:59)", back_kb())
        return

    await state.update_data(start_time=parsed.strftime("%H:%M"))
    await message.delete()

    await state.set_state(DoctorCreateStates.end_time)

    await safe_edit(state, message.from_user.id, "Введите время окончания:", back_kb())


# =========================
# END TIME + CONFIRM
# =========================

@router.message(DoctorCreateStates.end_time)
async def end_time(message: Message, state: FSMContext):
    if message.text.lower() == "назад":
        return await go_back(state, message.from_user.id, "Введите время начала:")

    parsed = parse_time(message.text)

    if not parsed:
        await safe_edit(state, message.from_user.id, "❌ Время должно быть в формате HH:MM", back_kb())
        return

    data = await state.get_data()

    start = data.get("start_time")

    # сравнение времени
    if start and parsed.strftime("%H:%M") <= start:
        await safe_edit(state, message.from_user.id, "❌ Время окончания должно быть позже начала", back_kb())
        return

    await state.update_data(end_time=parsed.strftime("%H:%M"))
    await message.delete()

    data = await state.get_data()

    text = (
        "Проверь данные:\n\n"
        f"ФИО: {data.get('full_name')}\n"
        f"Специализация ID: {data.get('specialization_id')}\n"
        f"Кабинет: {data.get('cabinet') or '—'}\n"
        f"График: {data.get('day_of_week')} {data.get('start_time')}-{data.get('end_time')}\n\n"
        "Подтвердить?"
    )

    await state.set_state(DoctorCreateStates.confirm)

    await safe_edit(state, message.from_user.id, text, confirm_kb())


# =========================
# CONFIRM
# =========================

@router.callback_query(F.data == "doc:no")
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Создание врача отменено")


@router.callback_query(F.data == "doc:yes")
async def confirm(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    text = (
        "👨‍⚕️ Карточка врача\n"
        f"ФИО: {data.get('full_name')}\n"
        f"Специализация ID: {data.get('specialization_id')}\n"
        f"Кабинет: {data.get('cabinet') or '—'}\n"
        f"График: {data.get('day_of_week')} {data.get('start_time')}-{data.get('end_time')}"
    )

    await state.clear()
    await call.message.edit_text(text)


@router.callback_query(F.data == "doc:back")
async def back_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    history = data.get("history", [])

    if not history:
        await call.answer("Вы на первом шаге")
        return

    history.pop()
    await state.update_data(history=history)

    current_state = await state.get_state()

    # простой rollback логики
    if current_state == DoctorCreateStates.specialization_id.state:
        await state.set_state(DoctorCreateStates.full_name)
        text = "Введите ФИО врача:"

    elif current_state == DoctorCreateStates.cabinet.state:
        await state.set_state(DoctorCreateStates.specialization_id)
        text = "Введите ID специализации:"

    elif current_state == DoctorCreateStates.day_of_week.state:
        await state.set_state(DoctorCreateStates.cabinet)
        text = "Введите кабинет:"

    elif current_state == DoctorCreateStates.start_time.state:
        await state.set_state(DoctorCreateStates.day_of_week)
        text = "Введите день недели:"

    elif current_state == DoctorCreateStates.end_time.state:
        await state.set_state(DoctorCreateStates.start_time)
        text = "Введите время начала:"

    else:
        await call.answer("Нельзя вернуться дальше")
        return

    await safe_edit(state, call.from_user.id, text, back_kb())
    await call.answer()