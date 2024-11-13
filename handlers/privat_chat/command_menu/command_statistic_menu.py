from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from database.tables.table_program import orm_get_last_program
from database.tables.table_program_file import orm_check_completed_days
from middlewares.DelMessages import MessageLoggingMiddleware

statistic_program_router = Router()


@statistic_program_router.message(Command('statistic'))
async def handle_statistic_training(message: Message, logger: MessageLoggingMiddleware, session: AsyncSession,
                                    bot: Bot):
    await logger.del_all_messages(bot, message)
    program_id = await orm_get_last_program(session, message.from_user.id)
    training_list = []
    if program_id:
        training_list = await orm_check_completed_days(session, program_id[0])
    if training_list:
        text = ""
        for program_data in training_list:
            training_number, program_status = program_data
            if program_status == "fail":
                program_status = "Невдача"
            else:
                program_status = "Успіх"

            text += f"Номер тренування№{training_number}\nРезультат тренування: {program_status}\n\n"
        event = await message.answer(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Назад🔙", callback_data=f"check_program")]]))
    else:
        text = "У вас не має тренувань!"
        event = await message.answer(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Назад🔙", callback_data=f"main_menu")]]))

    await logger.add_message(event)
