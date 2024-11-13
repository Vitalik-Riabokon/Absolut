from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.program_interface_buttons.start_menu_batton import main_menu
from middlewares.DelMessages import MessageLoggingMiddleware

main_menu_router = Router()


@main_menu_router.message(Command('menu'))
async def handle_menu(message: Message, logger: MessageLoggingMiddleware, bot: Bot, session: AsyncSession):
    await logger.del_all_messages(bot, message)
    event = await message.answer("Вітаю🖐️ Що бажаєте?", reply_markup=await main_menu())
    await logger.add_message(event)
