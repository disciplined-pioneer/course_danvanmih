from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.handlers.user.start import cmd_start


router = Router()


# Удаление сообщений, не подключённых к состоянию
@router.message()
async def handle_unexpected_message(message: types.Message, state: FSMContext):
    
    if message.text == '/start':
        await cmd_start(message, state)
        return

    print('🛑 Удаляем сообщение - не в состоянии 🛑')
    await message.delete()    
    