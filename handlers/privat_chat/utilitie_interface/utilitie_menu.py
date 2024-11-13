from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from buttons.utilities_interface_buttons.utilitie_menu_button import utilities_menu
from middlewares.DelMessages import MessageLoggingMiddleware

utilities_router = Router()


@utilities_router.callback_query(F.data == "utilities")
async def handler_program_menu(callback_query: CallbackQuery, bot: Bot, logger: MessageLoggingMiddleware,
                               state: FSMContext):
    await logger.del_all_messages(bot, callback_query.message)
    await state.clear()
    await callback_query.message.answer("Що бажаєш дізнатись?", reply_markup=await utilities_menu())
