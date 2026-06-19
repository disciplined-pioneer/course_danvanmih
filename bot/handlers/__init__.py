from bot.handlers.start import router as start
from bot.handlers.commands import router as commands
from bot.handlers.add_doctor import router as add_doctor
from bot.handlers.appointments_info import router as appointments_info
from bot.handlers.add_patient import router as  add_patient
from bot.handlers.doctor_search import router as doctor_search
from bot.handlers.patient_search import router as patient_search
from bot.handlers.doctor_schedule import router as doctor_schedule
from bot.handlers.clear_state import router as clear_state

routers = [
    start,
    commands,
    add_doctor,
    add_patient,
    appointments_info,
    doctor_search,
    patient_search,
    doctor_schedule,
    clear_state
]