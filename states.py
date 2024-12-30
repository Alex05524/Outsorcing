from aiogram.fsm.state import State, StatesGroup

class OrderForm(StatesGroup):
    full_name = State()
    address = State()
    phone_number = State()
    reason = State()

class StatusForm(StatesGroup):
    request_id = State()

class ReviewForm(StatesGroup):
    review = State()