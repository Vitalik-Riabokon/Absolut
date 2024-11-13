from aiogram.types import (InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def utilities_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Нормативи🥇", callback_data="regulations"
        ),
        InlineKeyboardButton(
            text="Коефіціент Wilks✨", callback_data="wilks"

        ),
        InlineKeyboardButton(
            text="Разовий максимум💯", callback_data="one_max"

        ),
        InlineKeyboardButton(
            text="Головне меню🔙", callback_data="main_menu"
        )
    )
    keyboard.adjust(1, 1)
    return keyboard.as_markup()
