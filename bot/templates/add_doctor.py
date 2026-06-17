enter_full_name = "Введите ФИО врача:"
enter_spec_id = "Введите ID специализации:"
enter_cabinet = "Введите кабинет:"
enter_day = "Введите дни недели работы в формате: ПН-ПТ"
enter_start_time = "Введите время начала:"
enter_end_time = "Введите время окончания:"
confirm_text = "Подтвердить?"

error_id = "❌ ID должен быть числом"
error_time_format = "❌ Время должно быть в формате HH:MM (00:00–23:59)"
error_end_time = "❌ Время окончания должно быть позже начала"

cancelled = "❌ Создание врача отменено"
no_back = "Вы на первом шаге"

def doctor_card(data):
    return (
        "👨‍⚕️ Создана новая карточка врача\n"
        f"ФИО: {data.get('full_name')}\n"
        f"Специализация ID: {data.get('specialization_id')}\n"
        f"Кабинет: {data.get('cabinet') or '—'}\n"
        f"График: {data.get('day_of_week')} {data.get('start_time')}-{data.get('end_time')}"
    )