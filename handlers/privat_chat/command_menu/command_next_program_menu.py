from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.table_program import orm_get_last_program
from database.tables.table_program_file import orm_next_check_days
from handlers.privat_chat.command_menu.command_last_program_menu import handle_last_training
from middlewares.DelMessages import MessageLoggingMiddleware

next_program_router = Router()


@next_program_router.message(Command('next'))
async def handle_next_training(message: Message, logger: MessageLoggingMiddleware, session: AsyncSession, bot: Bot):
    await logger.del_all_messages(bot, message)
    program_id = await orm_get_last_program(session, message.from_user.id)
    if program_id:
        training_number = await orm_next_check_days(session, program_id[0])
        print('🚫🚫', training_number)
        if training_number:
            event = await handle_last_training(message, logger, session, bot, data=training_number)
        else:
            event = await message.answer(text='Тренування вже пройдене, змініть програму',
                                         reply_markup=InlineKeyboardMarkup(
                                             inline_keyboard=[
                                                 [InlineKeyboardButton(text="Зрозуміло✨", callback_data="main_menu")],
                                             ]
                                         ))
    else:
        event = await message.answer(text='У вас не має програм тренування', reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Зрозуміло✨", callback_data="main_menu")],
            ]
        ))
    await logger.add_message(event)
