from datetime import datetime

from sqlalchemy import (DECIMAL, BigInteger, ForeignKey, DateTime)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    register_data: Mapped[datetime.date] = mapped_column(DateTime, nullable=False)

    # Реляція з Program
    programs: Mapped[list["Program"]] = relationship(
        "Program",
        back_populates="programs_user",
        cascade="all, delete-orphan"
    )


class Program(Base):
    __tablename__ = 'programs'
    program_id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'), nullable=False)
    program_name: Mapped[str] = mapped_column(nullable=False)
    program_file: Mapped[str] = mapped_column(nullable=False)
    program_date: Mapped[datetime.date] = mapped_column(DateTime, nullable=False)
    program_status: Mapped[str | None]

    # Реляція з ProgramFile
    program_files: Mapped[list["ProgramFile"]] = relationship(
        "ProgramFile",
        back_populates="program_files_program",
        cascade="all, delete-orphan"  # Каскадне видалення
    )

    programs_user: Mapped["User"] = relationship(
        back_populates="programs"
    )


class ProgramFile(Base):
    __tablename__ = 'program_files'
    program_file_id: Mapped[int] = mapped_column(primary_key=True)
    program_id: Mapped[int] = mapped_column(ForeignKey('programs.program_id'), nullable=False)
    training_number: Mapped[int] = mapped_column(nullable=False)
    approaches_number: Mapped[str] = mapped_column(nullable=False)
    repetitions_number: Mapped[str] = mapped_column(nullable=False)
    weight: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    program_status: Mapped[str | None] = mapped_column()

    program_files_program: Mapped["Program"] = relationship(
        "Program",
        back_populates="program_files"
    )
