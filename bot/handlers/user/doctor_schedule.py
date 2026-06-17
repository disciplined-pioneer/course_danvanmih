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
