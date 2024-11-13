from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.table_program_file import orm_get_program_files


async def training_pagination_buttons(current_page, program_id, total_pages):
    training_buttons = []
    if current_page > 0:
        training_buttons.append(
            InlineKeyboardButton(
                text="Назад⏪", callback_data=f"training_page_{program_id}_{current_page - 1}"
            )
        )
    if current_page < total_pages - 1:
        training_buttons.append(
            InlineKeyboardButton(
                text="Далі⏩", callback_data=f"training_page_{program_id}_{current_page + 1}"
            )
        )
    return training_buttons


async def get_training_day_buttons(session: AsyncSession, program_id: int,
                                   page: int = 0, training_list: list | None = None):
    if page == 0:
        items_per_page = 6
        start_index = page * items_per_page
    else:
        items_per_page = 9
        start_index = page * items_per_page - 3

    if training_list is None:
        training_list = await orm_get_program_files(session=session, program_id=program_id)

    end_index = start_index + items_per_page
    page_items = training_list[start_index:end_index]

    keyboard = InlineKeyboardBuilder()

    for training_number in page_items:
        if training_number in await orm_get_program_files(session=session, program_id=program_id):
            keyboard.add(
                InlineKeyboardButton(
                    text=f"№{training_number}",
                    callback_data=f"training_number_{training_number}",
                )
            )
    keyboard.adjust(3, 3)

    total_pages = (len(training_list) + items_per_page - 1) // items_per_page
    pagination_buttons = await training_pagination_buttons(page, program_id, total_pages)

    if pagination_buttons:
        keyboard.row(*pagination_buttons)
    if page == 0:
        keyboard.row(InlineKeyboardButton(text="Пошук🔎", callback_data=f"search_training_number_{program_id}"))
        keyboard.row(InlineKeyboardButton(text="Видалити програму💀", callback_data=f"del_program_{program_id}"))
        keyboard.row(InlineKeyboardButton(text="Змінити програму⌛", callback_data="change_program"))

    keyboard.row(InlineKeyboardButton(text="Меню Прогами🔙", callback_data="main_programs"))

    return keyboard.as_markup()
