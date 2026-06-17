from bot.handlers.user.start import router as start
from bot.handlers.user.doctor_search import router as doctor_search
from bot.handlers.user.doctor_schedule import router as doctor_schedule
from bot.handlers.user.clear_state import router as clear_state

routers = [
    start,
    doctor_search,
    doctor_schedule,
    clear_state
]