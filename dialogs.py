from aiogram.dispatcher.filters.state import StatesGroup, State

class GoalPreferenceParser(StatesGroup):
    mode = State()
    sort_by = State()