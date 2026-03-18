from aiogram.fsm.state import StatesGroup,State

class AddPro(StatesGroup):
    name=State()
    price=State()
    description=State()