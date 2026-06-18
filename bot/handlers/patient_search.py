from datetime import datetime
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from utils import patient_search as u
from bot.templates import patient_search as t
from bot.keyboards import patient_search as k

from db.models.models import Appointments, Patients


router = Router()


# Обработка кнопки "Поиск пациента"
@router.callback_query(F.data == "patient_search")
async def patient_search(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    await state.set_state(None)

    keyb, text = await k.buttons_with_all_patients()
    await callback.message.edit_text(
        text=text,
        reply_markup=keyb
    )


# Обработка кнопки выбора пациента
@router.callback_query(F.data.startswith("patient_id:"))
async def patient_id(callback: types.CallbackQuery, state: FSMContext):

    patient_id = int(callback.data.split(':')[1])
    await callback.message.edit_text(
        text=await t.build_patient_card(patient_id),
        reply_markup=await k.patient_delete_keyb()
    )
    await state.update_data(patient_id=patient_id)


# Обработка кнопки "Изменить адрес"
@router.callback_query(F.data == "change_address")
async def change_address(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    data = await state.get_data()
    patient_id = data.get('patient_id')

    msg = await callback.message.edit_text(
        text=t.new_address_text,
        reply_markup=await k.info_patient_keyb(patient_id=patient_id)
    )

    await state.set_state(u.AppointmentStates.new_address)
    await state.update_data(last_id_message=msg.message_id)


# Обработка нового адреса
@router.message(u.AppointmentStates.new_address)
async def new_address(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    patient_id = data.get('patient_id')
    patient_info = await Patients.get(id_patient=patient_id)
    await patient_info.update(address=message.text.strip())
    
    await u.safe_edit(state, message.from_user.id, t.new_patient_address, k.back_user_keyb)
    await state.clear()


# Удаление пациента
@router.callback_query(F.data == "delete_patient")
async def patient_delete(callback: types.CallbackQuery, state: FSMContext):

    # Удаление информации о докторе
    data = await state.get_data()
    patient_id = data.get('patient_id', None)
    name_patient, result = await u.delete_info_patient(patient_id)
    
    if result:
        await callback.message.edit_text(
            text=t.patient_deleted_message(name_patient),
            reply_markup=k.back_user_keyb
        )
    else:
        await callback.message.edit_text(
            text=t.patient_delete_error,
            reply_markup=k.back_user_keyb
        )


# Обработка кнопки добавления приёма
@router.callback_query(F.data == "add_appointment")
async def add_appointment(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    patient_id = data.get('patient_id', None)
    keyb, text = await k.buttons_with_all_doctors(patient_id)
    await callback.message.edit_text(
        text=text,
        reply_markup=keyb
    )


# Выбор врача для приёма
@router.callback_query(F.data.startswith("doctor_id_appointment:"))
async def select_doctor(callback: types.CallbackQuery, state: FSMContext):

    doctor_id = int(callback.data.split(":")[1])

    await state.update_data(doctor_id=doctor_id)
    await state.set_state(u.AppointmentStates.datetime)

    msg = await callback.message.edit_text(
        text=t.enter_datetime,
        reply_markup=k.back_doctor_list_keyb
    )
    await callback.answer()
    await state.update_data(doctor_id=doctor_id, last_id_message=msg.message_id)


# Обработка времени и даты
@router.message(u.AppointmentStates.datetime)
async def set_datetime(message: types.Message, state: FSMContext):

    await message.delete()

    try:
        dt = datetime.strptime(message.text.strip(), "%Y-%m-%d %H:%M")
    except:
        await u.safe_edit(state, message.from_user.id, t.error_datetime_format, k.back_doctor_list_keyb)
        return

    data = await state.get_data()

    await Appointments.add(
        patient_id=data["patient_id"],
        doctor_id=data["doctor_id"],
        appointment_date=dt.date(),
        appointment_time=dt.time(),
    )

    await u.safe_edit(state, message.from_user.id, t.appointment_created, k.back_user_keyb)
    await state.clear()