from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.bot import bot
from bot.keyboards.user.start import *
from bot.templates.user.start import *


router = Router()


# Обработка входящих сообщений
@router.message(Command("start", ignore_case=True))
async def cmd_start(message: Message, state: FSMContext):

    await message.answer(
        text=starting_user_message,
        reply_markup=start_user_keyb
    )