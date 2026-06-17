from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.templates import appointments_info as t
from bot.keyboards import appointments_info as k


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
    text = await t.build_doctor_appointments_text(doctor_id_appts)

    await callback.message.edit_text(
        text=text,
        reply_markup=k.back_user_keyb
    )
    await callback.answer()