from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from utils import doctor_search as u
from bot.templates import doctor_search as t
from bot.keyboards import doctor_search as k

from db.models.models import Doctors


router = Router()


# Обработка кнопки "Поиск врача"
@router.callback_query(F.data == "doctor_search")
async def doctor_search(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    await state.set_state(None)

    keyb, text = await k.buttons_with_all_doctors()
    await callback.message.edit_text(
        text=text,
        reply_markup=keyb
    )


# Обработка кнопки выбора врача
@router.callback_query(F.data.startswith("doctor_id:"))
async def doctor_id(callback: types.CallbackQuery, state: FSMContext):

    doctor_id = int(callback.data.split(':')[1])
    await callback.message.edit_text(
        text=await t.build_doctor_card(doctor_id),
        reply_markup=await k.doctor_delete_keyb()
    )
    await state.update_data(doctor_id=doctor_id)


# Обработка кнопки "Изменить кабинет"
@router.callback_query(F.data == "change_cabinet")
async def change_cabinet(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    data = await state.get_data()
    doctor_id = data.get('doctor_id')

    msg = await callback.message.edit_text(
        text=t.new_cabinet_text,
        reply_markup=await k.info_doctor_keyb(doctor_id=doctor_id)
    )

    await state.set_state(u.DoctorInfoStates.new_cabinet)
    await state.update_data(last_id_message=msg.message_id)


# Обработка нового номера кабинета
@router.message(u.DoctorInfoStates.new_cabinet)
async def new_cabinet(message: types.Message, state: FSMContext):

    await message.delete()
    data = await state.get_data()
    doctor_id = data.get('doctor_id')
    doctor_info = await Doctors.get(id_doctor=doctor_id)
    await doctor_info.update(cabinet=message.text.strip())
    
    await u.safe_edit(state, message.from_user.id, t.new_doctor_cabinet, k.back_user_keyb)
    await state.clear()


# Удаление врача
@router.callback_query(F.data == "delete_doctor")
async def doctor_delete(callback: types.CallbackQuery, state: FSMContext):

    # Удаление информации о докторе
    data = await state.get_data()
    doctor_id = data.get('doctor_id')
    name_doctor, result = await u.delete_info_doctor(doctor_id)
    
    if result:
        await callback.message.edit_text(
            text=t.doctor_deleted_message(name_doctor),
            reply_markup=k.back_user_keyb
        )
    else:
        await callback.message.edit_text(
            text=t.doctor_delete_error,
            reply_markup=k.back_user_keyb
        )