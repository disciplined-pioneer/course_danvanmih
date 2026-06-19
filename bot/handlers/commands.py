from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.types import Message

from db.models.models import Doctors, Patients
from bot.templates import commands as t
from bot.keyboards.doctor_search import doctor_edit_keyb
from bot.keyboards.patient_search import patient_delete_keyb


router = Router()


# Поиск врача
@router.message(Command("search_doctor", ignore_case=True))
async def search_doctor(
    message: Message,
    command: CommandObject
):
    fio = command.args
    if not fio:
        await message.answer(
            "Укажите ФИО врача:\n/search_doctor Иванов Иван Иванович"
        )
        return
    
    # Поиск всех врачей по фамилии
    doctors_info = await Doctors.filter(full_name=fio)
    if not doctors_info:
        await message.answer(
            text='Доктор не был найден'
        )
        return
    for doc in doctors_info:
        await message.answer(
            text=await t.format_doctor_card(doc),
            reply_markup=await doctor_edit_keyb(doc.id_doctor)
        )


# Поиск пациента
@router.message(Command("search_patient", ignore_case=True))
async def search_patient(
    message: Message,
    command: CommandObject
):
    fio = command.args

    if not fio:
        await message.answer(
            "Укажите ФИО пациента:\n/search_patient Иванов Иван Иванович"
        )
        return
    
    patients_info = await Patients.filter(full_name=fio)
    for pt in patients_info:
        await message.answer(
            text=await t.format_patient_card(pt),
            reply_markup=await patient_delete_keyb(pt.id_patient)
        )