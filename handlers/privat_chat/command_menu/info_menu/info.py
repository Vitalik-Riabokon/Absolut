import os

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, FSInputFile)

from middlewares.DelMessages import MessageLoggingMiddleware

info_router = Router()


@info_router.message(Command('info'))
async def handler_info(message: Message, bot: Bot, logger: MessageLoggingMiddleware, data='', text_size: int = 0):
    await logger.print_all_messages()
    await logger.del_all_messages(bot, message)

    file_name = 'info_photo.png'

    for root, dirs, files in os.walk('.'):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            break

    photo = FSInputFile(file_path)

    if data:
        data = 'Ви натрапили на помилку за номером: ' + data + f'\nРозмір назви файлу: {text_size}' + '\n'

    event = await message.answer_photo(photo=photo,
                                       caption=data + "\nСлідуйте за інструкцією для уникнення проблем з файлом:"
                                                      "\n\n1. Лист з програмою тренуванян повинен бути під назвою 'Тренування'"
                                                      "\n\n2. Заголовок для кожної колонки повиненн відповідати назвам вказаним на зображенні"
                                                      "\n\n3. Назва файла повинна розділятися пробіломи та не повинне перевищувати більше 50 байт! (помилка 2 часто як наслідок від 3)"
                                                      '''\n\n✅ Правильно: 'Легкий жим лежачи' (32 байти)
                                                         \n❌ Неправильно: 'Програма_Жим_Лежачи' (підкреслення замість пробілів)
                                                       \n4. Формат файлу:
                                                         \n✅ Правильно: program.xlsx
                                                         \n❌ Неправильно: program.xls, program.csv, program.txt'''
                                                      "\n\nБажаю вам успіхів✨",
                                       reply_markup=InlineKeyboardMarkup(
                                           inline_keyboard=[
                                               [InlineKeyboardButton(text="Зрозуміло✨", callback_data="main_menu")],
                                           ]
                                       ))

    await logger.add_message(event)
