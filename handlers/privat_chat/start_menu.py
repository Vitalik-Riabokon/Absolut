from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.program_interface_buttons.start_menu_batton import main_menu
from database.tables.table_user import orm_add_user, orm_get_user_id_by_telegram_id
from middlewares.DelMessages import MessageLoggingMiddleware

start_router = Router()


@start_router.message(Command('start'))
async def handle_start(message: Message, logger: MessageLoggingMiddleware, session: AsyncSession, bot: Bot):
    await message.delete()
    await logger.del_all_messages(bot, message)
    await message.answer("Вас вітає Absolute bot💪"
                         "\n\n/menu - Ваше головне меню"
                         "\n\n/statistic - Статистика успішності для останньої програми"
                         "\n\n/last - останнє тренування, яке отримало відмітку"
                         "\n\n/next - наступне тренування"
                         "\n\n/info - детально про стандартизацію")

    if await orm_get_user_id_by_telegram_id(session, message.from_user.id) is None:
        await orm_add_user(session=session, telegram_id=message.from_user.id)


@start_router.callback_query(F.data == 'main_menu')
async def handle_main_menu(callback_query: CallbackQuery, logger: MessageLoggingMiddleware, bot: Bot):
    await logger.del_all_messages(bot, callback_query.message)
    event = await callback_query.message.answer("Вітаю🖐️ Що бажаєте?", reply_markup=await main_menu())
    await logger.add_message(event)


@start_router.message(~F.text.startswith('/'), default_state)
async def handle_all_messages(message: Message, logger: MessageLoggingMiddleware, bot: Bot):
    await logger.print_all_messages()
    await logger.del_all_messages(bot, message)
    event = await message.answer("Вітаю🖐️ Що бажаєте?", reply_markup=await main_menu())

    await logger.add_message(event)
