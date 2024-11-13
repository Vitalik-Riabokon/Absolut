from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.table_program import orm_get_programs


async def program_pagination_buttons(current_page, total_pages):
    program_buttons = []
    if current_page > 0:
        program_buttons.append(
            InlineKeyboardButton(
                text="Назад⏪", callback_data=f"program_page_{current_page - 1}"
            )
        )
    if current_page < total_pages - 1:
        program_buttons.append(
            InlineKeyboardButton(
                text="Далі⏩", callback_data=f"program_page_{current_page + 1}"
            )
        )
    return program_buttons


async def get_program_buttons(session: AsyncSession, telegram_id: int, page: int = 0, program_list: list | None = None):
    if page == 0:
        items_per_page = 4
        start_index = page * items_per_page
    else:
        items_per_page = 6
        start_index = page * items_per_page - 2

    if program_list is None:
        program_list = await orm_get_programs(session=session, telegram_id=telegram_id)

    end_index = start_index + items_per_page
    page_items = program_list[start_index:end_index]

    keyboard = InlineKeyboardBuilder()

    if page_items:
        for program in page_items:
            keyboard.add(
                InlineKeyboardButton(
                    text=f"{program.program_name}",
                    callback_data=f"program_id_{program.program_id}",
                )
            )
    keyboard.adjust(1, 1)

    total_pages = (len(program_list) + items_per_page - 1) // items_per_page
    pagination_buttons = await program_pagination_buttons(page, total_pages)

    if pagination_buttons:
        keyboard.row(*pagination_buttons)
    if page == 0:
        keyboard.row(InlineKeyboardButton(text="Пошук🔎", callback_data=f"search_program"))

    keyboard.row(InlineKeyboardButton(text="Меню Прогами🔙", callback_data="check_program"))

    return keyboard.as_markup()
