from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models.models import Specializations


async def buttons_with_all_specializations():
    specs = await Specializations.all()

    if not specs:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]]
        ), '❕ Пока нет доступных врачей'

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=s.name, callback_data=f'spec_name:{s.id_specialization}')]
            for s in specs
        ] + [[InlineKeyboardButton(text='🔙 Меню', callback_data='back_start_menu')]]
    ), 'Выберите специализацию врача'