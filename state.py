from aiogram.fsm.state import StatesGroup, State

class App(StatesGroup):
    name = State()
    phone = State()
    category = State()
    time = State()
    payment = State()

class Drive(StatesGroup):
    d_name = State()
    d_phone = State()
    d_stage = State()
    d_type_car = State()
    d_amount = State()
    d_time = State()

