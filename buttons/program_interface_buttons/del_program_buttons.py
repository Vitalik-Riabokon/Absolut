from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def confirmation_buttons(program_id: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Так",
                    callback_data=f"delete_successfully_{program_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Ні", callback_data=f"check_program"
                )
            ],
        ]
    )
    return keyboard
