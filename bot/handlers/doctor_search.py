from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from utils import doctor_search as u
from bot.templates import doctor_search as t
from bot.keyboards import doctor_search as k


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
        reply_markup=await k.doctor_delete_keyb(doctor_id)
    )


# Удаление врача
@router.callback_query(F.data.startswith("delete_doctor:"))
async def doctor_delete(callback: types.CallbackQuery, state: FSMContext):

    # Удаление информации о докторе
    doctor_id = int(callback.data.split(':')[1])
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