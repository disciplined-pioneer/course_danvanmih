from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from utils import add_patient as u
from bot.templates import add_patient as t
from bot.keyboards import add_patient as k
from db.models.models import Patients


router = Router()


# Добавить пациента
@router.callback_query(F.data == "add_patient")
async def start(call: types.CallbackQuery, state: FSMContext):

    await state.clear()
    msg = await call.message.edit_text(
        text=t.enter_full_name,
        reply_markup=k.back_user_keyb
    )

    await state.set_state(u.PatientCreateStates.full_name)
    await state.update_data(last_id_message=msg.message_id)

    await call.answer()


# ФИО
@router.message(u.PatientCreateStates.full_name)
async def full_name(message: types.Message, state: FSMContext):
    await message.delete()

    await state.update_data(full_name=message.text)
    await state.set_state(u.PatientCreateStates.address)

    await u.safe_edit(
        state,
        message.from_user.id,
        t.enter_address,
        k.back_kb()
    )


# Адрес
@router.message(u.PatientCreateStates.address)
async def address(message: types.Message, state: FSMContext):
    await message.delete()

    await state.update_data(address=message.text)
    await state.set_state(u.PatientCreateStates.birth_date)

    await u.safe_edit(
        state,
        message.from_user.id,
        t.enter_birth_date,
        k.back_kb()
    )


# Дата рождения
@router.message(u.PatientCreateStates.birth_date)
async def birth_date(message: types.Message, state: FSMContext):
    await message.delete()

    parsed = u.parse_date(message.text)

    if not parsed:
        await u.safe_edit(
            state,
            message.from_user.id,
            t.error_birth_date,
            k.back_kb()
        )
        return

    await state.update_data(birth_date=parsed)
    await state.set_state(u.PatientCreateStates.phone)

    await u.safe_edit(
        state,
        message.from_user.id,
        t.enter_phone,
        k.back_kb()
    )


# Телефон
@router.message(u.PatientCreateStates.phone)
async def phone(message: types.Message, state: FSMContext):
    await message.delete()

    parsed = u.parse_phone(message.text)

    if not parsed:
        await u.safe_edit(
            state,
            message.from_user.id,
            t.error_phone,
            k.back_kb()
        )
        return

    await state.update_data(phone=parsed)
    await state.set_state(u.PatientCreateStates.confirm)

    data = await state.get_data()
    text = t.patient_card(data)
    await u.safe_edit(
        state,
        message.from_user.id,
        t.confirm_text + text,
        k.confirm_kb()
    )


# Confirm
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
    await call.message.edit_text(
        text=t.patient_card(data),
        reply_markup=k.back_user_keyb
    )
    await call.answer()


# Добавление врача отменено
@router.callback_query(F.data == "patient:no")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        text=t.cancelled,
        reply_markup=k.back_user_keyb
    )


# Обработка кнопки "Назад" (пациенты)
@router.callback_query(F.data == "patient:back")
async def back_handler(call: types.CallbackQuery, state: FSMContext):

    current_state = await state.get_state()

    # rollback логики пациента
    if current_state == u.PatientCreateStates.address.state:
        await state.set_state(u.PatientCreateStates.full_name)
        text = t.enter_full_name

    elif current_state == u.PatientCreateStates.birth_date.state:
        await state.set_state(u.PatientCreateStates.address)
        text = t.enter_address

    elif current_state == u.PatientCreateStates.phone.state:
        await state.set_state(u.PatientCreateStates.birth_date)
        text = t.enter_birth_date

    elif current_state == u.PatientCreateStates.confirm.state:
        await state.set_state(u.PatientCreateStates.phone)
        text = t.enter_phone

    else:
        await call.answer("Нельзя вернуться назад")
        return

    await u.safe_edit(
        state,
        call.from_user.id,
        text,
        k.back_kb()
    )

    await call.answer()