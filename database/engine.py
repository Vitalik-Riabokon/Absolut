import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from database.models import Base

load_dotenv()
async_engine = create_async_engine(
    os.getenv('URL'), echo=True
)

async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def update_sequence(tabla_value: str, table_name: str, sequence_name: str):
    async with async_engine.begin() as session:
        # Знайти максимальне значення таблиці
        result = await session.execute(text(f"SELECT MAX({tabla_value}) FROM {table_name}"))
        max_value = result.scalar() or 0

        # Перевірка типу бази даних
        if "sqlite" in async_engine.url.drivername:
            # Перевіряємо, чи існує таблиця sqlite_sequence
            table_exists = await session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
            )
            if table_exists.scalar() is not None:
                # Оновлюємо значення автоінкременту
                await session.execute(text(f"UPDATE sqlite_sequence SET seq = :max_value WHERE name = :table_name"),
                                      {"max_value": max_value, "table_name": table_name})
        elif "postgresql" in async_engine.url.drivername:
            # Для PostgreSQL використовуємо setval для послідовності
            await session.execute(text(f"SELECT setval('{sequence_name}', :max_value + 1, false)"),
                                  {"max_value": max_value})



async def create_tables():
    async with async_engine.begin() as session:
        await session.run_sync(Base.metadata.create_all)
        async_engine.echo = True


async def drop_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
