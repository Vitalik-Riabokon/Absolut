import os
import re
from datetime import datetime

import pandas as pd
from aiogram import Bot, Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, Document, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.program_interface_buttons.programs_menu_button import program_menu
from database.tables.table_program import orm_add_program
from database.tables.table_program_file import orm_add_program_file
from handlers.privat_chat.command_menu.info_menu.info import handler_info
from middlewares.DelMessages import MessageLoggingMiddleware

add_program_router = Router()


class FSMProgram(StatesGroup):
    program_file = State()


@add_program_router.callback_query(F.data == "add_program")
async def handler_program_menu(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        "Відповідно до умов стандартизації відправте файл .xlsx❕",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад🔙", callback_data="main_programs")],
            ]
        ), )
    await state.set_state(FSMProgram.program_file)


async def correct_filename(filename: str) -> str:
    """
    Виправляє назву файлу, щоб вона відповідала допустимому формату: великі літери на початку слів, пробіли між словами.

    :param filename: Назва файлу, яку потрібно виправити.
    :return: Виправлена назва файлу.
    """
    # Розділяємо назву файлу на ім'я і розширення
    name, ext = os.path.splitext(filename)

    # Замінюємо підкреслення на пробіли
    corrected_name = name.replace('_', ' ').capitalize()

    # Змінюємо текст на правильний формат
    return corrected_name


@add_program_router.message(FSMProgram.program_file)
async def handler_fms_program_file(message: Message, logger: MessageLoggingMiddleware, state: FSMContext, bot: Bot,
                                   session: AsyncSession):
    await state.clear()
    errors = []

    if message.content_type != ContentType.DOCUMENT or ".xlsx" not in message.document.file_name:
        errors.append('4')
    else:
        original_filename = message.document.file_name
        corrected_filename = await correct_filename(original_filename)
        text_size = len(corrected_filename.encode('utf-8'))
        if text_size > 50 or not bool(
                re.match('^[A-ZА-Я][a-zа-я]*(?: [a-zа-я0-9№]+)*$', corrected_filename)):
            errors.append('3')

        document: Document = message.document
        try:
            file_id = document.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            local_file_path = f"downloads/{corrected_filename}"
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            await bot.download_file(file_path, local_file_path)
        except Exception:
            errors.append('5')

        try:
            read_excel_file = pd.read_excel(local_file_path, sheet_name="Тренування", header=1)
        except Exception as e:
            errors.append('1')

        try:
            if not errors:
                program_file = message.document.file_id
                program_date = datetime.now().date()
                print("❗program_date program_file", program_date, program_file)
                program_id = await orm_add_program(
                    session=session,
                    telegram_id=message.from_user.id,
                    program_name=corrected_filename,
                    program_file=program_file,
                    program_date=program_date,
                    program_status='active'
                )
                print("❗program_id", program_id)

                await orm_add_program_file(session, program_id, read_excel_file)
                await logger.del_all_messages(bot, message)
                await message.answer(
                    text="Програма успішно добавлена",
                    reply_markup=await program_menu())
            else:
                raise Exception
        except Exception as e:
            print("❗❗Exception ", e)
            errors.append('2')

    if errors:
        error_message = ','.join(errors)
        await logger.del_all_messages(bot, message)
        await handler_info(message, bot, logger, data=error_message, text_size=text_size)
