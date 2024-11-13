from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.program_interface_buttons.change_program_button import get_program_buttons
from database.tables.table_program import orm_get_last_program, orm_get_programs, \
    orm_update_status
from handlers.privat_chat.program_interface.check_program_menu import handler_check_program
from middlewares.DelMessages import MessageLoggingMiddleware

change_program_router = Router()


class SearchProgram(StatesGroup):
    search_program = State()


@change_program_router.callback_query(F.data == "change_program")
async def handler_change_program(callback_query: CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text(
        text="Оберіть програму тренування👇",
        reply_markup=await get_program_buttons(session, telegram_id=callback_query.from_user.id))


@change_program_router.callback_query(lambda c: c.data.startswith("program_page_"))
async def handler_program_page(callback_query: CallbackQuery, session: AsyncSession):
    page = int(callback_query.data.split("_")[-1])
    await callback_query.message.edit_text(
        f"Оберіть програму тренування👇",
        reply_markup=await get_program_buttons(session=session, page=page,
                                               telegram_id=callback_query.from_user.id)
    )


@change_program_router.callback_query(lambda c: c.data.startswith("search_program"))
async def handler_search_programs(callback_query: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.set_state(SearchProgram.search_program)
    await callback_query.message.edit_text(
        text="Введіть введіть повну або чаткову назву програми:", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад🔙", callback_data="change_program")],
            ]
        ), )


@change_program_router.message(SearchProgram.search_program)
async def handler_search_program(
        message: Message, state: FSMContext, bot: Bot, session: AsyncSession, logger: MessageLoggingMiddleware
):
    program_list = []
    search_query = message.text.lower()

    all_programs = await orm_get_programs(session, message.from_user.id)

    for program in all_programs:
        program_name = program.program_name.lower()

        # Перевірка на повне співпадіння
        if search_query == program_name:
            program_list.append(program.program_name)
            continue

        # Перевірка на часткове співпадіння слів
        search_words = search_query.split()
        program_words = program_name.split()

        if all(any(search_word in prog_word for prog_word in program_words) for search_word in search_words):
            program_list.append(program)
            continue

        # Перевірка на часткове співпадіння підрядків
        if any(search_word in program_name for search_word in search_words):
            program_list.append(program)
            continue

        # Перевірка на співпадіння дати
        if any(word.replace('.', '') in program_name.replace('.', '') for word in search_words if
               word.replace('.', '').isdigit()):
            program_list.append(program)

    await message.answer(
        text="Оберіть програму:",
        reply_markup=await get_program_buttons(session=session, program_list=program_list,
                                               telegram_id=message.from_user.id))

    await logger.del_all_messages(bot, message)
    await state.clear()


@change_program_router.callback_query(lambda c: c.data.startswith("program_id_"))
async def handler_program_id(callback_query: CallbackQuery, session: AsyncSession, logger: MessageLoggingMiddleware,
                             bot: Bot, state: FSMContext):
    program_id = int(callback_query.data.split("_")[-1])
    last_program_id = await orm_get_last_program(session, callback_query.from_user.id)
    if last_program_id:
        await orm_update_status(session, last_program_id[0], None)
    await orm_update_status(session, program_id, 'active')
    await handler_check_program(callback_query=callback_query, logger=logger, bot=bot, session=session, state=state)
