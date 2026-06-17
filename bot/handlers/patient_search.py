from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from utils import patient_search as u
from bot.templates import patient_search as t
from bot.keyboards import patient_search as k


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
        reply_markup=await k.patient_delete_keyb(patient_id)
    )


# Удаление пациента
@router.callback_query(F.data.startswith("delete_patient:"))
async def patient_delete(callback: types.CallbackQuery, state: FSMContext):

    # Удаление информации о докторе
    patient_id = int(callback.data.split(':')[1])
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