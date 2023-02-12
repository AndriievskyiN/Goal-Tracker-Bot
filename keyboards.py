from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboard:
    @staticmethod
    def get_keyboard(type: str) -> InlineKeyboardMarkup:
        if type == "goal_mode_keyboard":
            text = {"Тиждень": "week", "Місяць": "month", "Рік": "year"}

        elif type == "goal_sort_by_keyboard":
            text = {"Виконані цілі": "completed_goals", "Заохочення": "rewards", "Не виконані цілі": "uncompleted_goals", "Всього цілей": "total_goals"}

        buttons = [InlineKeyboardButton(text=txt, callback_data=callback) for txt, callback in text.items()]
        keyboard = InlineKeyboardMarkup().add(*buttons)
        return keyboard
