from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import update_sequence
from database.models import User


async def orm_add_user(
        session: AsyncSession,
        telegram_id: int,
) -> None:
    """
    Додає користувача до бази даних.

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        telegram_id (int): Ідентифікатор користувача в Telegram.
        register_data (DataTime): Дата реєстрації користувача
    Результат:
        Створює новий запис у таблиці користувачів.
    """
    await update_sequence(tabla_value='user_id', table_name='users',
                          sequence_name="users_user_id_seq")
    time_now = datetime.now().date()
    new_user = User(
        telegram_id=telegram_id,
        register_data=time_now,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)


async def orm_get_user_id_by_telegram_id(
        session: AsyncSession, telegram_id: int
) -> Optional[User]:
    """
    Отримує дані користувача за його Telegram ID.

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        telegram_id (int): Ідентифікатор користувача в Telegram.

    Повертає:
        Optional[User]: дані про користувача або None, якщо користувача не знайдено.

    Результат:
        Отримує дані про користувача з таблиці користувачів.
    """
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    return user
