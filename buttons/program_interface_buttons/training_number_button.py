from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def success_check_button(training_number):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=f"Успіх", callback_data=f"success_check_{training_number}_success"),
        InlineKeyboardButton(text=f"Невдача", callback_data=f"success_check_{training_number}_fail"),
    )
    keyboard.adjust(1, 1)
    keyboard.row(
        InlineKeyboardButton(text=f"Назад🔙", callback_data=f"check_program")
    )
    return keyboard.as_markup()
