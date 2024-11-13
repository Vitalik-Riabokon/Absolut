from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.program_interface_buttons.programs_menu_button import program_menu
from middlewares.DelMessages import MessageLoggingMiddleware

router_programs_router = Router()


@router_programs_router.callback_query(F.data == "main_programs")
async def handler_program_menu(callback_query: CallbackQuery, bot: Bot, session: AsyncSession, state: FSMContext,
                               logger: MessageLoggingMiddleware):
    await state.clear()
    await callback_query.message.edit_text("Добавте або переглянте наявні програми", reply_markup=await program_menu())
