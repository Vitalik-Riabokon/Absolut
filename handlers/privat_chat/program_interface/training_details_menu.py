from aiogram import Router
from aiogram.types import (CallbackQuery)
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.program_interface_buttons.check_program_button import get_training_day_buttons
from buttons.program_interface_buttons.training_number_button import success_check_button
from database.tables.table_program import orm_get_last_program, orm_get_program
from database.tables.table_program_file import orm_get_program_file_data, orm_update_status_program_file

training_details_router = Router()


@training_details_router.callback_query(lambda c: c.data.startswith("training_number_"))
async def handler_training_number(callback_query: CallbackQuery, session: AsyncSession):
    training_number = int(callback_query.data.split("_")[-1])
    program_id = await orm_get_last_program(session, callback_query.from_user.id)
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
    await callback_query.message.edit_text(
        text=response, reply_markup=await success_check_button(training_number)
    )


@training_details_router.callback_query(lambda c: c.data.startswith("success_check_"))
async def handler_internal_detailing_program(
        callback_query: CallbackQuery, session: AsyncSession
):
    training_number, type_training = int(callback_query.data.split("_")[-2]), callback_query.data.split("_")[-1]
    program_id = await orm_get_last_program(session, callback_query.from_user.id)

    await orm_update_status_program_file(
        session=session,
        program_status=type_training,
        program_id=program_id[0],
        training_number=training_number,
    )

    program = await orm_get_program(session, program_id[0], callback_query.from_user.id)
    await callback_query.message.edit_text(
        f'Всі ваші тренувальні дні до нещодавно добавленої програми\n\nНазва програми: \n👉 {program[0].program_name}',
        reply_markup=await get_training_day_buttons(session, program_id[0]))
