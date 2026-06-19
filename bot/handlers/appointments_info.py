from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.templates import appointments_info as t
from bot.keyboards import appointments_info as k
from utils import add_patient as u

from db.models.models import Appointments


router = Router()


# Обработка кнопки "Сведения о приёмах"
@router.callback_query(F.data == "appointments_info")
async def appointments_info(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    await state.set_state(None)

    keyb, text = await k.doctors_appts_kb()
    await callback.message.edit_text(
        text=text,
        reply_markup=keyb
    )


# Обработка кнопки выбора приёмов врача
@router.callback_query(F.data.startswith("doctor_id_appts:"))
async def doctor_id_appts(callback: types.CallbackQuery, state: FSMContext):

    doctor_id_appts = int(callback.data.split(':')[1])
    text, keyb = await k.get_doctor_appointments(doctor_id_appts)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyb
    )
    await state.update_data(doctor_id_appts=doctor_id_appts)
    await callback.answer()


# Переходим по приёму
@router.callback_query(F.data.startswith("app_id_info:"))
async def app_id_info(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    app_id = int(callback.data.split(':')[1])
    doctor_id_appts = data.get('doctor_id_appts')
    
    await callback.message.edit_text(
        text=await t.build_appointment_text(app_id),
        reply_markup=await k.doctor_appointment_actions_kb(doctor_id_appts)
    )
    await state.update_data(app_id=app_id)
    await callback.answer()


# Обработка кнопки "Удалить приём"
@router.callback_query(F.data == "delete_appointment")
async def delete_appointment(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    app_id = data.get('app_id')

    app_info = await Appointments.get(id_appointment=app_id)
    await app_info.delete()

    await callback.message.edit_text(
        text=t.delete_app_text,
        reply_markup=k.back_user_keyb
    )


# Обработка кнопки "Изменить диагноз"
@router.callback_query(F.data == "change_diagnosis")
async def change_diagnosis(callback: types.CallbackQuery, state: FSMContext):

    msg = await callback.message.edit_text(
        text='Введите новое значение диагноза',
    )
    await state.set_state(u.DiagnosisStates.new_diagnosis)
    await state.update_data(last_id_message=msg.message_id)


# Обработка нового номера диагноза
@router.message(u.DiagnosisStates.new_diagnosis)
async def new_diagnosis(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    app_id = data.get('app_id')
    
    app_info = await Appointments.get(id_appointment=app_id)
    await app_info.update(diagnosis=message.text.strip())
    
    await u.safe_edit(state, message.from_user.id, 'Диагноз был изменён', k.back_user_keyb)
    await state.clear()