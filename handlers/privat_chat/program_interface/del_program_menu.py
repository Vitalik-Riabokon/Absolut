from aiogram import Router
from aiogram.types import (CallbackQuery)
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.program_interface_buttons.change_program_button import get_program_buttons
from buttons.program_interface_buttons.del_program_buttons import confirmation_buttons
from database.tables.table_program import del_program

del_program_router = Router()


@del_program_router.callback_query(lambda c: c.data.startswith("del_program_"))
async def handler_del_program(callback_query: CallbackQuery, session: AsyncSession):
    program_id = int(callback_query.data.split("_")[-1])
    await callback_query.message.edit_text(
        f"Оберіть програму тренування👇",
        reply_markup=await confirmation_buttons(program_id)
    )


@del_program_router.callback_query(lambda c: c.data.startswith("delete_successfully_"))
async def handler_delete_successfully(callback_query: CallbackQuery, session: AsyncSession):
    program_id = int(callback_query.data.split("_")[-1])
    await del_program(session, program_id)
    await callback_query.message.edit_text(
        f"Оберіть програму тренування👇",
        reply_markup=await get_program_buttons(session=session, telegram_id=callback_query.from_user.id)
    )
