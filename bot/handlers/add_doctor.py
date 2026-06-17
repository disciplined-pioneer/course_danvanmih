from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from utils import add_doctor as u
from bot.keyboards import add_doctor as k


router = Router()


# Обработка кнопки "Добавить доктора"
@router.callback_query(F.data == "add_doctor")
async def start(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(history=[])

    msg = await call.message.edit_text("Введите ФИО врача:")

    await state.set_state(u.DoctorCreateStates.full_name)
    await state.update_data(last_id_message=msg.message_id)


# Обработка сообщения ФИО
@router.message(u.DoctorCreateStates.full_name)
async def full_name(message: Message, state: FSMContext):

    await message.delete()
    if message.text.lower() == "назад":
        return await u.go_back(state, message.from_user.id, "Введите ФИО врача:")

    await state.update_data(full_name=message.text)

    data = await state.get_data()
    data["history"].append("full_name")
    await state.update_data(history=data["history"])

    await state.set_state(u.DoctorCreateStates.specialization_id)

    await u.safe_edit(state, message.from_user.id, "Введите ID специализации:", k.back_kb())


# Обработка сообщения специализации
@router.message(u.DoctorCreateStates.specialization_id)
async def spec(message: Message, state: FSMContext):

    await message.delete()
    if message.text.lower() == "назад":
        return await u.go_back(state, message.from_user.id, "Введите ФИО врача:")

    if not message.text.isdigit():
        await u.safe_edit(state, message.from_user.id, "❌ ID должен быть числом", k.back_kb())
        return

    await state.update_data(specialization_id=int(message.text))

    data = await state.get_data()
    data["history"].append("spec")
    await state.update_data(history=data["history"])

    await state.set_state(u.DoctorCreateStates.cabinet)

    await u.safe_edit(state, message.from_user.id, "Введите кабинет (или '-'):", k.back_kb())


# Обработка номера кабинета
@router.message(u.DoctorCreateStates.cabinet)
async def cabinet(message: Message, state: FSMContext):

    await message.delete()
    if message.text.lower() == "назад":
        return await u.go_back(state, message.from_user.id, "Введите ID специализации:")

    await state.update_data(cabinet=None if message.text == "-" else message.text)

    data = await state.get_data()
    data["history"].append("cabinet")
    await state.update_data(history=data["history"])

    await state.set_state(u.DoctorCreateStates.day_of_week)

    await u.safe_edit(state, message.from_user.id, "Введите день недели:", k.back_kb())


# Обработка дня недели
@router.message(u.DoctorCreateStates.day_of_week)
async def day(message: Message, state: FSMContext):

    await message.delete()
    if message.text.lower() == "назад":
        return await u.go_back(state, message.from_user.id, "Введите кабинет:")

    await state.update_data(day_of_week=message.text)

    await state.set_state(u.DoctorCreateStates.start_time)

    await u.safe_edit(state, message.from_user.id, "Введите время начала:", k.back_kb())


# Начало времени работа
@router.message(u.DoctorCreateStates.start_time)
async def start_time(message: Message, state: FSMContext):

    await message.delete()
    if message.text.lower() == "назад":
        return await u.go_back(state, message.from_user.id, "Введите день недели:")

    parsed = u.parse_time(message.text)

    if not parsed:
        await u.safe_edit(state, message.from_user.id, "❌ Время должно быть в формате HH:MM (00:00–23:59)", k.back_kb())
        return

    await state.update_data(start_time=parsed.strftime("%H:%M"))

    await state.set_state(u.DoctorCreateStates.end_time)

    await u.safe_edit(state, message.from_user.id, "Введите время окончания:", k.back_kb())


# Конец времени работы
@router.message(u.DoctorCreateStates.end_time)
async def end_time(message: Message, state: FSMContext):

    await message.delete()
    if message.text.lower() == "назад":
        return await u.go_back(state, message.from_user.id, "Введите время начала:")

    parsed = u.parse_time(message.text)

    if not parsed:
        await u.safe_edit(state, message.from_user.id, "❌ Время должно быть в формате HH:MM", k.back_kb())
        return

    data = await state.get_data()

    start = data.get("start_time")

    # сравнение времени
    if start and parsed.strftime("%H:%M") <= start:
        await u.safe_edit(state, message.from_user.id, "❌ Время окончания должно быть позже начала", k.back_kb())
        return

    await state.update_data(end_time=parsed.strftime("%H:%M"))
    data = await state.get_data()

    text = (
        "Проверь данные:\n\n"
        f"ФИО: {data.get('full_name')}\n"
        f"Специализация ID: {data.get('specialization_id')}\n"
        f"Кабинет: {data.get('cabinet') or '—'}\n"
        f"График: {data.get('day_of_week')} {data.get('start_time')}-{data.get('end_time')}\n\n"
        "Подтвердить?"
    )

    await state.set_state(u.DoctorCreateStates.confirm)

    await u.safe_edit(state, message.from_user.id, text, k.confirm_kb())


# Добавление врача отменено
@router.callback_query(F.data == "doc:no")
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("❌ Создание врача отменено")


# Создать врача - да
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


# Обработка кнопки "Назад"
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
    if current_state == u.DoctorCreateStates.specialization_id.state:
        await state.set_state(u.DoctorCreateStates.full_name)
        text = "Введите ФИО врача:"

    elif current_state == u.DoctorCreateStates.cabinet.state:
        await state.set_state(u.DoctorCreateStates.specialization_id)
        text = "Введите ID специализации:"

    elif current_state == u.DoctorCreateStates.day_of_week.state:
        await state.set_state(u.DoctorCreateStates.cabinet)
        text = "Введите кабинет:"

    elif current_state == u.DoctorCreateStates.start_time.state:
        await state.set_state(u.DoctorCreateStates.day_of_week)
        text = "Введите день недели:"

    elif current_state == u.DoctorCreateStates.end_time.state:
        await state.set_state(u.DoctorCreateStates.start_time)
        text = "Введите время начала:"

    else:
        await call.answer("Нельзя вернуться дальше")
        return

    await u.safe_edit(state, call.from_user.id, text, k.back_kb())
    await call.answer()