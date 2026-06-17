import re
from datetime import datetime
from aiogram.fsm.state import StatesGroup, State

class PatientCreateStates(StatesGroup):
    full_name = State()
    address = State()
    birth_date = State()
    phone = State()
    confirm = State()

def parse_date(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except:
        return None


def parse_phone(value: str):
    # очень простая проверка (не усложняй без нужды)
    if re.match(r"^\+?\d{10,15}$", value):
        return value
    return None