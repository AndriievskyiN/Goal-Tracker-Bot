from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboard:
    def __init__(self, name):
        pass

    @staticmethod
    def goal_mode_keyboard():
        text = {"Тиждень": "week", "Місяць": "month", "Рік": "year"}

        buttons = [InlineKeyboardButton(text=txt, callback_data=callback) for txt, callback in text.items()]
        keyboard = InlineKeyboardMarkup().add(*buttons)
        return keyboard
    
    @staticmethod
    def goal_sort_by_keyboard():
        text = {"Виконані цілі": "completed", "Заохочення": "rewards", "Не виконані цілі": "uncompleted", "Всього цілей": "total"}

        buttons = [InlineKeyboardButton(text=txt, callback_data=callback) for txt, callback in text.items()]
        keyboard = InlineKeyboardMarkup().add(*buttons)
        return keyboard
