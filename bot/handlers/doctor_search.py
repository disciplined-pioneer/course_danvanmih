from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from utils import doctor_search as u
from bot.templates import doctor_search as t
from bot.keyboards import doctor_search as k

from db.models.models import Doctors, Schedules, Patients, Specializations


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
        reply_markup=await k.doctor_edit_keyb(doctor_id)
    )
    await state.update_data(doctor_id=doctor_id)


# Выбор редактирования
@router.callback_query(F.data.startswith(("edit_doctor", "edit_schedule", "edit_patient")))
async def start_edit(callback: types.CallbackQuery, state: FSMContext):

    prefix, obj_id, field = callback.data.split(":")

    obj_id = int(obj_id)

    if prefix == "edit_doctor":
        fields = k.DOCTOR_FIELDS
    elif prefix == "edit_patient":
        fields = k.PATIENT_FIELDS
    else:
        fields = k.SCHEDULE_FIELDS

    field_info = fields[field]

    await state.update_data(
        obj_id=obj_id,
        field=field,
        model=prefix
    )

    await state.set_state(u.EditState.value)
    await callback.message.edit_text(
        f'Введите новое значение для: "{field_info["label"]}"'
    )


# Обработка нового значения
@router.message(u.EditState.value)
async def process_edit_value(message: types.Message, state: FSMContext):

    data = await state.get_data()

    obj_id = data["obj_id"]
    field = data["field"]
    model = data["model"]

    value = message.text.strip()

    if model == "edit_doctor":
        fields = k.DOCTOR_FIELDS
        model = Doctors

        # Поиск и создание новой специализации
        if field == 'specialization_id':
            value = value.lower()
            spec_info = await Specializations.get(name=value)
            if not spec_info:
                spec_info = await Specializations.create(name=value)
            value = spec_info.id_specialization

    elif model == "edit_schedule":
        fields = k.SCHEDULE_FIELDS
        model = Schedules

    elif model == "edit_patient":
        fields = k.PATIENT_FIELDS
        model = Patients

    else:
        await message.answer("❌ Неизвестная модель")
        await state.clear()
        return

    field_info = fields[field]
    field_type = field_info.get("type", "text")

    try:
        if field_type == "int":
            value = int(value)

        elif field_type == "time":
            from datetime import time as dt_time
            h, m = map(int, value.split(":"))
            value = dt_time(h, m)

        elif field_type == "select":
            value = int(value)

        elif field == "birth_date":
            from datetime import datetime
            value = datetime.strptime(value, "%Y-%m-%d").date()

    except Exception:
        await message.answer("❌ Неверный формат данных")
        return

    await model.update_obj(obj_id, **{field: value})
    await message.answer(f"✅ Обновлено: {field_info['label']}")

    await state.clear()


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