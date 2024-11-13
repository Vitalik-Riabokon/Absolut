from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message

from buttons.utilities_interface_buttons.one_max_menu_button import one_max_menu_button
from middlewares.DelMessages import MessageLoggingMiddleware

one_max_router = Router()


class FSMOneMax(StatesGroup):
    type_formula = State()
    barbell_weight = State()
    number_repetitions = State()


@one_max_router.callback_query(F.data == "one_max")
async def handler_one_max(callback_query: CallbackQuery, bot: Bot, logger: MessageLoggingMiddleware, state: FSMContext):
    await logger.del_all_messages(bot, callback_query.message)
    await state.clear()
    await callback_query.message.answer("Оберіть формулу для розрахунків: ",
                                        reply_markup=await one_max_menu_button())


@one_max_router.callback_query(lambda c: c.data.startswith("formula_"))
async def handler_one_max(callback_query: CallbackQuery, bot: Bot, logger: MessageLoggingMiddleware, state: FSMContext):
    type_formula = callback_query.data.split("_")[-1]
    await state.update_data(type_formula=type_formula)
    event = await callback_query.message.edit_text("Введіть вагу штанги:", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад🔙",
                                  callback_data="one_max")],
        ]
    ))
    await logger.add_message(event)
    await state.set_state(FSMOneMax.barbell_weight)


@one_max_router.message(FSMOneMax.barbell_weight)
async def handler_one_max(message: Message, bot: Bot, logger: MessageLoggingMiddleware, state: FSMContext):
    if not message.text.isdigit():
        event = await message.answer("Введіть число!", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад🔙",
                                      callback_data="one_max")],
            ]
        ))
    else:
        await state.update_data(barbell_weight=int(message.text))
        event = await message.answer("Введіть кількість повторів:", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад🔙",
                                      callback_data="one_max")],
            ]
        ), )
        await state.set_state(FSMOneMax.number_repetitions)
    await logger.add_message(event)


@one_max_router.message(FSMOneMax.number_repetitions)
async def handler_one_max(message: Message, bot: Bot, logger: MessageLoggingMiddleware, state: FSMContext):
    if not message.text.isdigit():
        event = await message.answer("Введіть число!", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Назад🔙",
                                      callback_data="one_max")],
            ]
        ))
    else:
        await logger.del_all_messages(bot, message)
        data = await state.get_data()
        await state.clear()
        type_formula = data["type_formula"]
        if type_formula == 'wendler':
            result = data['barbell_weight'] / (1.0278 - 0.0278 * int(message.text))

        else:
            result = data['barbell_weight'] * (36 / (37 - int(message.text)))

        event = await message.answer(f"Ваш результат: {round(result, 2)}",
                                     reply_markup=await one_max_menu_button())
    await logger.add_message(event)
