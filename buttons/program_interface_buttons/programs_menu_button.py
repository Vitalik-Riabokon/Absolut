from aiogram.types import (InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def program_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="Добавити програму", callback_data="add_program"),
        InlineKeyboardButton(
            text="Огляд програми", callback_data="check_program"
        ),
        InlineKeyboardButton(
            text="Головне меню🔙", callback_data="main_menu"
        )
    )
    keyboard.adjust(1, 1)
    return keyboard.as_markup()

