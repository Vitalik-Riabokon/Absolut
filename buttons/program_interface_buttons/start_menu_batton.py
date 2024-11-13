from aiogram.types import (InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def main_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Програми", callback_data="main_programs"),
        InlineKeyboardButton(
            text="Утиліти", callback_data="utilities"
        ))
    keyboard.adjust(1, 1)
    return keyboard.as_markup()

