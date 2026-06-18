from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.templates import start as t
from bot.keyboards import start as k


router = Router()


# Обработка входящих сообщений
@router.message(Command("start", ignore_case=True))
async def cmd_start(message: Message, state: FSMContext):

    await message.answer(
        text=t.starting_user_message,
        reply_markup=k.start_user_keyb
    )

    await message.delete()


# Обработка кнопки "Меню"
@router.callback_query(F.data == "back_start_menu")
async def back_start_menu(callback: types.CallbackQuery, state: FSMContext):

    await callback.answer()
    await state.set_state(None)
    await callback.message.edit_text(
        text=t.starting_user_message,
        reply_markup=k.start_user_keyb
    )