from datetime import datetime
from typing import Optional

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import update_sequence
from database.models import Program


async def orm_add_program(
        session: AsyncSession,
        telegram_id: int,
        program_name: str,
        program_file: str,
        program_date: datetime.date,
        program_status
) -> int:
    """
    Додає нову програму до бази даних. Змінює статус попередньої програми на неакативну null

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        telegram_id (int): Ідентифікатор користувача у телеграмі.
        program_file (str): Файл програми.
        program_date (datetime): Дата програми.
        program_status (str): статус програми активний або null

    Повертає:
        int: Ідентифікатор нової програми.
    """
    await update_sequence(tabla_value='program_id', table_name='programs',
                          sequence_name="programs_program_id_seq")

    program_id = await orm_get_last_program(session, telegram_id)

    if program_id:
        await orm_update_status(session, program_id[0], None)

    new_program = Program(
        telegram_id=telegram_id,
        program_name=program_name,
        program_file=program_file,
        program_date=program_date,
        program_status=program_status
    )
    session.add(new_program)
    await session.commit()
    return new_program.program_id


async def orm_update_status(session: AsyncSession, program_id: int, program_status: Optional[str] = None) -> None:
    """
    Оновлює статус програми на не активний

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        program_id (int): номер тренувальної програми
    """
    stmt = (
        update(Program)
        .where(Program.program_id == program_id)
        .values(program_status=program_status)
    )
    await session.execute(stmt)
    await session.commit()


async def orm_get_last_program(
        session: AsyncSession, telegram_id: int) -> tuple[int]:
    """
    Повертає останню тренувальну програму у базі

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.

    Повертає:
        program_id tuple[int]: номер тренувальної програми

    """
    res = await session.execute(
        select(Program.program_id)
        .where(Program.telegram_id == telegram_id)
        .where(Program.program_status == 'active')
    )
    return res.fetchone()


async def orm_get_program(
        session: AsyncSession, program_id: int, telegram_id: int) -> list[Optional[Program]]:
    """
    Повертає обєкт програми який містить всю інформацію програми відповідно за індентифікатор програми

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        program_id (int): індентифікатор програми

    Повертає:
        Program: list[Optional[Program]]: обєкт програми

    """
    res = await session.execute(
        select(Program)
        .where(Program.program_id == program_id)
        .where(Program.telegram_id == telegram_id)
    )
    return res.fetchone()


async def orm_get_programs(session: AsyncSession, telegram_id: int) -> list[Optional[Program]]:
    """
    Повертає всі наявні програми упорядковіні від нової до старої по даті

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.

    Повертає:
        list[Optional[Program]]: Упорядкований список обектів програм.
    """
    result = await session.execute(
        select(Program)
        .where(Program.telegram_id == telegram_id)
        .order_by(Program.program_date.asc())
    )
    res = result.fetchall()
    if res:
        return [res[0] for res in res]


async def del_program(session: AsyncSession, program_id: int) -> None:
    """
    Видаляє програму з бази за її індентифікатором

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        program_id (int): індентифікатор програми
    """
    await session.execute(
        delete(Program).where(Program.program_id == program_id)
    )
    await session.commit()
