import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from dotenv import load_dotenv

from database.engine import async_session, create_tables
from handlers.privat_chat.command_menu.command_last_program_menu import last_program_router
from handlers.privat_chat.command_menu.command_main_menu import main_menu_router
from handlers.privat_chat.command_menu.command_next_program_menu import next_program_router
from handlers.privat_chat.command_menu.command_statistic_menu import statistic_program_router
from handlers.privat_chat.command_menu.info_menu.info import info_router
from handlers.privat_chat.program_interface.add_program_menu import add_program_router
from handlers.privat_chat.program_interface.change_program_menu import change_program_router
from handlers.privat_chat.program_interface.check_program_menu import check_program_router
from handlers.privat_chat.program_interface.del_program_menu import del_program_router
from handlers.privat_chat.program_interface.programs_menu import router_programs_router
from handlers.privat_chat.program_interface.training_details_menu import training_details_router
from handlers.privat_chat.start_menu import start_router
from handlers.privat_chat.utilitie_interface.one_max_menu import one_max_router
from handlers.privat_chat.utilitie_interface.regulations_menu import regulations_router
from handlers.privat_chat.utilitie_interface.utilitie_menu import utilities_router
from handlers.privat_chat.utilitie_interface.wilks_menu import wilks_router
from middlewares.DelMessages import MessageLoggingMiddleware
from middlewares.SessionAlchamy import DataBaseSession

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

# Створюємо один екземпляр middleware для всього роутера
message_logger = MessageLoggingMiddleware()
dp.message.middleware(message_logger)
dp.callback_query.middleware(message_logger)

dp.include_routers(start_router, router_programs_router,
                   add_program_router, info_router,
                   check_program_router, change_program_router,
                   del_program_router, training_details_router,
                   last_program_router, main_menu_router,
                   next_program_router, statistic_program_router,
                   utilities_router, regulations_router,
                   wilks_router, one_max_router)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


async def set_commands(bot: Bot):
    private_chat_commands = [
        BotCommand(command="/start", description="Меню реєстрації"),
        BotCommand(command="/menu", description="Головне меню"),
        BotCommand(command="/statistic", description="Статистика успішності для останньої програми"),
        BotCommand(command="/next", description="Наступне тренування"),
        BotCommand(command="/last", description="Останннє тренування"),
        BotCommand(command="/info", description="Інструкція користування"),
    ]

    await bot.set_my_commands(
        private_chat_commands
    )


async def on_startup():
    logging.info("Бот запущено")
    # await drop_db()
    await create_tables()


async def main():
    await set_commands(bot)
    dp.startup.register(on_startup)
    dp.update.middleware(DataBaseSession(session_pool=async_session))
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Polling was cancelled")
    finally:
        await bot.session.close()
        dp.shutdown()


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
