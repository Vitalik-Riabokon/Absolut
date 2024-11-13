from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from sqlalchemy.ext.asyncio import AsyncSession

from buttons.utilities_interface_buttons.utilitie_menu_button import utilities_menu
from middlewares.DelMessages import MessageLoggingMiddleware

wilks_router = Router()


class FSMWilks(StatesGroup):
    user_weight = State()
    barbell_weight = State()


@wilks_router.callback_query(F.data == "wilks")
async def handler_wilks(callback_query: CallbackQuery, bot: Bot, session: AsyncSession, state: FSMContext):
    await callback_query.message.edit_text("Введіть вагу атлета:", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад🔙",
                                  callback_data="utilities")],
        ]
    ), )
    await state.set_state(FSMWilks.user_weight)


@wilks_router.message(FSMWilks.user_weight)
async def handler_user_weight(message: Message, bot: Bot, logger: MessageLoggingMiddleware, state: FSMContext):
    if not message.text.isdigit():
        event = await message.answer("Введіть число!", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад🔙",
                                      callback_data="utilities")],
            ]
        ))
    else:
        await logger.del_all_messages(bot, message)
        await state.update_data(user_weight=int(message.text))
        event = await message.answer("Введіть вагу штанги:", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад🔙",
                                      callback_data="utilities")],
            ]
        ), )
        await state.set_state(FSMWilks.barbell_weight)
    await logger.add_message(event)


async def calculate_wilks(x, y):
    a = -216.0475144
    b = 16.2606339
    c = -0.002388645
    d = -0.00113732
    e = 7.01863E-06
    f = -1.291E-08
    # Обчислення коефіцієнта k
    k = 500 / (a + b * x + c * x ** 2 + d * x ** 3 + e * x ** 4 + f * x ** 5)

    # Обчислення Wilks
    wilks = y * k

    return wilks


@wilks_router.message(FSMWilks.barbell_weight)
async def handler_barbell_weight(message: Message, bot: Bot, logger: MessageLoggingMiddleware, state: FSMContext):
    if not message.text.isdigit():
        event = await message.answer("Введіть число!", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад🔙",
                                      callback_data="utilities")],
            ]
        ))
    else:
        await logger.del_all_messages(bot, message)

        data = await state.get_data()
        await state.clear()
        barbell_weight = int(message.text)

        wilks_result = await calculate_wilks(data['user_weight'], barbell_weight)

        event = await message.answer(text=f'Ваш результат: {round(wilks_result, 4)}',
                                     reply_markup=await utilities_menu())
    await logger.add_message(event)
