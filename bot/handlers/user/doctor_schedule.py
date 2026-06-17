from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from core.bot import bot
from settings import settings

from bot.templates.user import doctor_schedule as t
from bot.keyboards.user import doctor_schedule as k



router = Router()


# Обработка кнопки "Выбор специализации"
@router.callback_query(F.data == "doctor_schedule")
async def doctor_schedule(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    await state.set_state(None)

    keyb, text = await k.buttons_with_all_specializations()
    await callback.message.edit_text(
        text=text,
        reply_markup=keyb
    )


# Обработка кнопки выбора специальности
@router.callback_query(F.data.startswith("spec_id:"))
async def spec_id(callback: types.CallbackQuery, state: FSMContext):

    spec_id = int(callback.data.split(':')[1])
    await callback.message.edit_text(
        text=await t.list_doctors_spec(spec_id),
        reply_markup=k.back_list_specializations
    )
    
    await state.update_data(spec_id=spec_id)


# Обработка кнопки выбора врача
@router.callback_query(F.data.startswith("doctor_id:"))
async def doctor_id_id(callback: types.CallbackQuery, state: FSMContext):

    doctor_id_id = int(callback.data.split(':')[1])
    keyb, text = await k.buttons_with_doctors_by_specialization(spec_id=spec_id)
    await callback.message.edit_text(
        text=text,
        reply_markup=keyb
    )
    
    await state.update_data(spec_id=spec_id)