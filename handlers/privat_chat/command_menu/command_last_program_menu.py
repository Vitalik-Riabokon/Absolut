from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.program_interface_buttons.training_number_button import success_check_button
from database.tables.table_program import orm_get_last_program
from database.tables.table_program_file import orm_check_completed_days, orm_get_program_file_data
from middlewares.DelMessages import MessageLoggingMiddleware

last_program_router = Router()


@last_program_router.message(Command('last'))
async def handle_last_training(message: Message, logger: MessageLoggingMiddleware, session: AsyncSession, bot: Bot,
                               data: list[tuple[int]] | None = None):
    await logger.del_all_messages(bot, message)
    program_id = await orm_get_last_program(session, message.from_user.id)
    training_number = 0
    if program_id:
        if data is None:
            program = await orm_check_completed_days(session, program_id[0])
            print("👉👉", program)
            if program:
                training_number, _ = program[0]
        else:
            training_number = data[0][0]
    if program_id and training_number:
        program_data = await orm_get_program_file_data(session=session, program_id=program_id[0],
                                                       training_number=training_number)
        response = ''
        if program_data:
            response = f"Дані про тренування №{training_number}:\n"
            for row in program_data:
                approaches_number, repetitions_number, weight, program_status = row

                response += f"Кількість підходів: {approaches_number}, Повтори: {repetitions_number}, Вага: {weight}\n"
            if program_status == 'success':
                program_status = '\nСтатус програми: Успіх\n\n'
            elif program_status == 'fail':
                program_status = '\nСтатус програми: Невдача\n\n'
            else:
                program_status = ''
            response += program_status

        event = await message.answer(text=response, reply_markup=await success_check_button(training_number))
    else:
        event = await message.answer(text='У вас не має програм тренування', reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Зрозуміло✨", callback_data="main_menu")],
            ]
        ))
    await logger.add_message(event)
