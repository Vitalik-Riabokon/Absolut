from aiogram.types import (InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def one_max_menu_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Wendler", callback_data="formula_wendler"
        ),
        InlineKeyboardButton(
            text="Brzycki", callback_data="formula_brzycki")
        ,
        InlineKeyboardButton(
            text="Назад🔙", callback_data="utilities")
    )

    keyboard.adjust(1, 1)
    return keyboard.as_markup()
