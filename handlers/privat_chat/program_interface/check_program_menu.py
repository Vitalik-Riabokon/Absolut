from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.program_interface_buttons.check_program_button import get_training_day_buttons
from buttons.program_interface_buttons.programs_menu_button import program_menu
from buttons.program_interface_buttons.start_menu_batton import main_menu
from database.tables.table_program import orm_get_last_program, orm_get_program
from middlewares.DelMessages import MessageLoggingMiddleware

check_program_router = Router()


class Search(StatesGroup):
    search_training_number = State()


@check_program_router.callback_query(F.data == "check_program")
async def handler_check_program(callback_query: CallbackQuery, logger: MessageLoggingMiddleware, bot: Bot,
                                session: AsyncSession, state: FSMContext):
    await state.clear()
    program_id = await orm_get_last_program(session, callback_query.from_user.id)
    print('👉👉👉', program_id)
    print('👉👉👉', callback_query.from_user.id)
    if program_id:
        program = await orm_get_program(session, program_id[0], callback_query.from_user.id)
        event = await callback_query.message.edit_text(
            f'Всі ваші тренувальні дні до нещодавно добавленої програми\n\nНазва програми: \n👉 {program[0].program_name}',
            reply_markup=await get_training_day_buttons(session, program_id[0]))
        await logger.add_message(event)
    else:
        event = await callback_query.message.edit_text(
            f'Ви не маєте програми! Добавте програму', reply_markup=await main_menu())
        await logger.add_message(event)


@check_program_router.callback_query(lambda c: c.data.startswith("training_page_"))
async def handler_training_page(callback_query: CallbackQuery, session: AsyncSession):
    program_id, page = int(callback_query.data.split("_")[-2]), int(callback_query.data.split("_")[-1])
    program = await orm_get_program(session, program_id, callback_query.from_user.id)
    await callback_query.message.edit_text(
        f"Ім'я програми: \n👉 {program[0].program_name}:",
        reply_markup=await get_training_day_buttons(session=session, program_id=program_id, page=page)
    )


@check_program_router.callback_query(lambda c: c.data.startswith("search_training_number_"))
async def handler_search_training_number(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.set_state(Search.search_training_number)
    program_id = int(callback_query.data.split("_")[-1])
    await state.update_data(search_training_number=program_id)

    await callback_query.message.edit_text(
        text="Введіть номер тренування:", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад🔙", callback_data="check_program")],
            ]
        ), )


@check_program_router.message(Search.search_training_number)
async def handler_search_training_number(message: Message, state: FSMContext, bot: Bot, session: AsyncSession,
                                         logger: MessageLoggingMiddleware):
    training_list = []
    training_number = message.text
    if training_number.isdigit():
        await logger.del_all_messages(bot, message)
        training_list.append(int(training_number))
        data: dict = await state.get_data()
        event = await message.answer(
            text="Оберіть номер програми:",
            reply_markup=await get_training_day_buttons(session=session,
                                                        program_id=data['search_training_number'],
                                                        training_list=training_list))
        await state.clear()
    else:
        event = await message.answer(
            text="Номер тренування 👉 число: 1 або 14")
    await logger.add_message(event)
