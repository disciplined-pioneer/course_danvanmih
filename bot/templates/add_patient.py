enter_full_name = "Введите ФИО пациента:"
enter_address = "Введите адрес:"
enter_birth_date = "Введите дату рождения (YYYY-MM-DD) (2000-10-10):"
enter_phone = "Введите телефон:"

error_birth_date = "❌ Неверный формат даты. Введите в формате (YYYY-MM-DD) (2000-10-10)"
error_phone = "❌ Неверный телефон (+XXXXXXXXXXX)"

confirm_text = "Проверь данные:\n\n"
cancelled = "❌ Создание пациента отменено"
created = "Пациент создан"

def patient_card(data):
    return (
        "👤 Новая карточка пациента\n"
        f"ФИО: {data.get("full_name", '-')}\n"
        f"Адрес: {data.get("address", '-')}\n"
        f"Дата рождения: {data.get("birth_date", '-')}\n"
        f"Телефон: {data.get("phone", '-')}"
    )
    