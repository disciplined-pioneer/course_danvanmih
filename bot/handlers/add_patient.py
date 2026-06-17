from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from utils import add_patient as u
from bot.templates import add_patient as t
from bot.keyboards import add_patient as k
from db.models.models import Patients


router = Router()


# Добаваить пациента
@router.callback_query(F.data == "add_patient")
async def start(call: types.CallbackQuery, state: FSMContext):
    await state.clear()

    msg = await call.message.edit_text(
        "Введите ФИО пациента:",
    )

    await state.set_state(u.PatientCreateStates.full_name)
    await state.update_data(last_id_message=msg.message_id)

    await call.answer()


# ФИО пациента
@router.message(u.PatientCreateStates.full_name)
async def full_name(message: types.Message, state: FSMContext):
    await message.delete()

    await state.update_data(full_name=message.text)
    await state.set_state(u.PatientCreateStates.address)

    await message.answer("Введите адрес:")


# Адрес пациента
@router.message(u.PatientCreateStates.address)
async def address(message: types.Message, state: FSMContext):
    await message.delete()

    await state.update_data(address=message.text)
    await state.set_state(u.PatientCreateStates.birth_date)

    await message.answer("Введите дату рождения (YYYY-MM-DD):")


# Дата рождения
@router.message(u.PatientCreateStates.birth_date)
async def birth_date(message: types.Message, state: FSMContext):
    await message.delete()

    parsed = u.parse_date(message.text)
    if not parsed:
        await message.answer("❌ Формат: YYYY-MM-DD")
        return

    await state.update_data(birth_date=parsed)
    await state.set_state(u.PatientCreateStates.phone)

    await message.answer("Введите телефон:")


# Телефон пациента
@router.message(u.PatientCreateStates.phone)
async def phone(message: types.Message, state: FSMContext):
    await message.delete()

    parsed = u.parse_phone(message.text)
    if not parsed:
        await message.answer("❌ Неверный телефон (+XXXXXXXXXXX)")
        return

    await state.update_data(phone=parsed)
    await state.set_state(u.PatientCreateStates.confirm)

    data = await state.get_data()

    text = (
        "👤 Новый пациент\n"
        f"ФИО: {data['full_name']}\n"
        f"Адрес: {data['address']}\n"
        f"Дата рождения: {data['birth_date']}\n"
        f"Телефон: {data['phone']}"
    )

    await message.answer("Проверь данные:\n\n" + text, reply_markup=k.confirm_kb())


# Подтверждение
@router.callback_query(F.data == "patient:yes")
async def confirm(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await Patients.add(
        full_name=data["full_name"],
        address=data["address"],
        birth_date=data["birth_date"],
        phone=data["phone"],
    )

    await state.clear()

    await call.message.edit_text("Пациент создан")
    await call.answer()