from typing import List, Tuple

import pandas as pd
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import update_sequence
from database.models import ProgramFile


async def orm_add_program_file(
        session: AsyncSession, program_id: int, read_excel_file: pd.DataFrame
) -> None:
    """
    Додає деталі програми з файлу Excel до бази даних.

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        program_id (int): Ідентифікатор програми.
        read_excel_file (pd.DataFrame): Дані з файлу Excel.
    """
    try:
        await update_sequence(tabla_value='program_file_id', table_name='program_files',
                              sequence_name='program_files_program_file_id_seq')

        for index, row in read_excel_file.iterrows():
            print('➖')
            new_detail = ProgramFile(
                program_id=program_id,
                training_number=row["Тренировка№"],
                approaches_number=row["Кількість підходів"],
                repetitions_number=str(row["Повтори"]),
                weight=row["169,9"],
            )

            session.add(new_detail)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print('🏋️‍', e)
        raise e


async def orm_get_program_files(session: AsyncSession, program_id: int) -> list[int] | None:
    """
    Перевіряє тренувальні дні для даного ідентифікатора програми.

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        program_id (int): Ідентифікатор програми.

    Повертає:
        list[int]: Список даних (номер тренування,).
    """
    result = await session.execute(
        select(ProgramFile.training_number)
        .where(ProgramFile.program_id == program_id)
        .order_by(ProgramFile.training_number.asc())
        .distinct()
    )
    res = result.fetchall()
    if res:
        return [res[0] for res in res]


async def orm_next_check_days(session: AsyncSession, program_id: int) -> List[Tuple[int]] | None:
    """
    Надає наступну тренувальну програму, в якої статус null для даного ідентифікатора програми.

    Аргументи:
    session (AsyncSession): Асинхронна сесія SQLAlchemy.
    program_id (int): Ідентифікатор програми.

    Повертає:
    List[Tuple[int]]: Список номерів тренувань.
    """
    # Отримання останнього завершеного тренування
    program = await orm_check_completed_days(session=session, program_id=program_id)
    if program:
        training_number, _ = program[0]
    else:
        return None

    # Перевірка на наявність наступного тренування
    query = (select(ProgramFile.training_number)
             .where(ProgramFile.program_id == program_id)
             .where(ProgramFile.training_number == training_number + 1)  # Шукаємо наступне тренування
             .where(ProgramFile.program_status.is_(None))  # Статус повинен бути null
             .distinct())

    # Виконання запиту
    result = await session.execute(query)
    next_training = result.fetchone()

    # Перевірка, чи знайдено наступне тренування
    if next_training is None:
        return None  # Якщо тренування з номером `training_number + 1` не знайдено, повертаємо None
    return [next_training]


async def orm_check_completed_days(
        session: AsyncSession, program_id: int
) -> List[Tuple[int, str]]:
    """
    Перевіряє дні, в які була завершена програма для даного ідентифікатора програми.

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        program_id (int): Ідентифікатор програми.

    Повертає:
        List[Tuple[int, str]]: Список номерів тренувань та статусу.
    """

    result = await session.execute(
        select(ProgramFile.training_number, ProgramFile.program_status)
        .where(ProgramFile.program_id == program_id)
        .where(ProgramFile.program_status.isnot(None))
        .distinct()
        .order_by(ProgramFile.training_number.desc())
    )

    res = result.fetchall()

    return res


async def orm_get_program_file_data(
        session: AsyncSession, program_id: int, training_number: int
) -> List[Tuple[int, int, float, str]]:
    """
    Отримує дані деталей програми для заданого номера тренування та ідентифікатора програми.

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        program_id (int): Ідентифікатор програми.
        training_number (int): Номер тренування.

    Повертає:
        List[Tuple[int, int, float, str]]: Список даних (кількість підходів, кількість повторів, вага, статус програми).
    """
    result = await session.execute(
        select(
            ProgramFile.approaches_number,
            ProgramFile.repetitions_number,
            ProgramFile.weight,
            ProgramFile.program_status
        )
        .where(ProgramFile.training_number == training_number)
        .where(ProgramFile.program_id == program_id)
    )
    return result.fetchall()


async def orm_update_status_program_file(
        session: AsyncSession, program_id: int, training_number: int, program_status: str
) -> None:
    """
    Оновлює статус програми для даного ідентифікатора програми та номера тренування.

    Аргументи:
        session (AsyncSession): Асинхронна сесія SQLAlchemy.
        program_id (int): Ідентифікатор програми.
        training_number (int): Номер тренування.
        program_status (str): Новий статус програми.
    """
    try:
        await session.execute(
            update(ProgramFile)
            .where(ProgramFile.program_id == program_id)
            .where(ProgramFile.training_number == training_number)
            .values(program_status=program_status)
        )
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise e
