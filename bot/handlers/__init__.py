from bot.handlers.start import router as start
from bot.handlers.add_doctor import router as add_doctor
from bot.handlers.add_patient import router as  add_patient
from bot.handlers.doctor_search import router as doctor_search
from bot.handlers.doctor_schedule import router as doctor_schedule
from bot.handlers.clear_state import router as clear_state

routers = [
    start,
    add_doctor,
    add_patient,
    doctor_search,
    doctor_schedule,
    clear_state
]