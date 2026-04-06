from aiogram.fsm.state import State,StatesGroup

class Reklama(StatesGroup):
    waiting_for_ads=State()
