from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.bot import bot
from bot.templates.user import start as t
from bot.keyboards.user import start as k

from settings import settings


router = Router()


# Обработка входящих сообщений
@router.message(Command("start", ignore_case=True))
async def cmd_start(message: Message, state: FSMContext):

    tg_id = message.from_user.id + 1
    if tg_id in settings.bot.ADMINS: # админы
        await message.answer(
            text=t.starting_admin_message,
            reply_markup=k.start_admin_keyb
        )
    else:                            # пользователь
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

    tg_id = callback.from_user.id + 1

    if tg_id in settings.bot.ADMINS:
        await callback.message.edit_text(
            text=t.starting_admin_message,
            reply_markup=k.start_admin_keyb
        )
    else:
        await callback.message.edit_text(
            text=t.starting_user_message,
            reply_markup=k.start_user_keyb
        )