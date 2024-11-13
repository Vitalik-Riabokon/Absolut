import os

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.utilities_interface_buttons.regulations_menu_button import regulations_menu
from middlewares.DelMessages import MessageLoggingMiddleware

regulations_router = Router()


async def search_file(file_name: str) -> FSInputFile:
    for root, dirs, files in os.walk('.'):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            break

    return FSInputFile(file_path)


@regulations_router.callback_query(F.data == "regulations")
async def handler_regulations(callback_query: CallbackQuery, bot: Bot, session: AsyncSession,
                              logger: MessageLoggingMiddleware):
    await logger.del_all_messages(bot, callback_query.message)
    await callback_query.message.answer("Що бажаєш дізнатись?", reply_markup=await regulations_menu())


@regulations_router.callback_query(F.data == "strict_bips")
async def handler_strict_bips(callback_query: CallbackQuery, bot: Bot, session: AsyncSession, state: FSMContext):
    await callback_query.message.delete()
    file_name = 'Строгий біцпс.png'
    photo = await search_file(file_name)
    await callback_query.message.answer_photo(photo=photo,
                                              caption='Нормативи по строгому підйомі на біцепс без екіпіровки з допінг контролем',
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [InlineKeyboardButton(text="Назад🔙",
                                                                            callback_data="regulations")],
                                                  ]
                                              ), )


@regulations_router.callback_query(F.data == "army_press")
async def handler_army_press(callback_query: CallbackQuery, bot: Bot, session: AsyncSession, state: FSMContext):
    await callback_query.message.delete()
    file_name = 'Армійський жим.png'
    photo = await search_file(file_name)
    await callback_query.message.answer_photo(photo=photo,
                                              caption='Нормативи по армійському жимові без екіпіровки з допінг контролем',
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [InlineKeyboardButton(text="Назад🔙",
                                                                            callback_data="regulations")],
                                                  ]
                                              ), )


@regulations_router.callback_query(F.data == "deadlift")
async def handler_deadlift(callback_query: CallbackQuery, bot: Bot, session: AsyncSession, state: FSMContext):
    await callback_query.message.delete()
    file_name = 'Станова тяга.png'
    photo = await search_file(file_name)
    await callback_query.message.answer_photo(photo=photo,
                                              caption='Нормативи по станові тязі без екіпіровки з допінг контролем',
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [InlineKeyboardButton(text="Назад🔙",
                                                                            callback_data="regulations")],
                                                  ]
                                              ), )


@regulations_router.callback_query(F.data == "squat")
async def handler_squat(callback_query: CallbackQuery, bot: Bot, session: AsyncSession, state: FSMContext):
    await callback_query.message.delete()
    file_name = 'Присяд.png'
    photo = await search_file(file_name)
    await callback_query.message.answer_photo(photo=photo,
                                              caption='Нормативи по присяду без екіпіровки з допінг контролем',
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [InlineKeyboardButton(text="Назад🔙",
                                                                            callback_data="regulations")],
                                                  ]
                                              ), )


@regulations_router.callback_query(F.data == "bench_press")
async def handler_bench_press(callback_query: CallbackQuery, bot: Bot, session: AsyncSession, state: FSMContext):
    await callback_query.message.delete()
    file_name = 'Жим лежачи.png'
    photo = await search_file(file_name)
    await callback_query.message.answer_photo(photo=photo,
                                              caption='Нормативи по жиму лежачи без екіпіровки з допінг контролем',
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [InlineKeyboardButton(text="Назад🔙",
                                                                            callback_data="regulations")],
                                                  ]
                                              ), )


@regulations_router.callback_query(F.data == "tribalism")
async def handler_tribalism(callback_query: CallbackQuery, bot: Bot, session: AsyncSession, state: FSMContext):
    await callback_query.message.delete()
    file_name = 'Триборство.png'
    photo = await search_file(file_name)
    await callback_query.message.answer_photo(photo=photo,
                                              caption='Сума трьох вправ у кілограмаї з допінг контролем',
                                              reply_markup=InlineKeyboardMarkup(
                                                  inline_keyboard=[
                                                      [InlineKeyboardButton(text="Назад🔙",
                                                                            callback_data="regulations")],
                                                  ]
                                              ))
