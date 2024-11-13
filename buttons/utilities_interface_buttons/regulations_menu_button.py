from aiogram.types import (InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def regulations_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Строгий біцпс💪", callback_data="strict_bips"
        ),
        InlineKeyboardButton(
            text="Армійський жим🏋️‍♂️", callback_data="army_press"

        ),
        InlineKeyboardButton(
            text="Станова тяга✨", callback_data="deadlift"

        ),
        InlineKeyboardButton(
            text="Присяд✨", callback_data="squat"
        ),
        InlineKeyboardButton(
            text="Жим лежачи✨", callback_data="bench_press"
        ),
        InlineKeyboardButton(
            text="Триборство✨", callback_data="tribalism"
        ),
        InlineKeyboardButton(
            text="Назад🔙", callback_data="utilities"
        )
    )
    keyboard.adjust(2, 2)
    return keyboard.as_markup()
