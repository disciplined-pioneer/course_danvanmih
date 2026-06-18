from datetime import date, time
from typing import TypeVar, Generic, Sequence

from typing import Optional, List
from sqlalchemy import not_
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, case, desc, JSON, func, Boolean, ForeignKey

from sqlalchemy.orm import Mapped, selectinload, load_only, relationship
from sqlalchemy.sql import select, update as sqlalchemy_update

from db.models.mapped_columns import *
from core.psql import async_db_session, Base


T = TypeVar("T")


class ModelAdmin(Generic[T]):
    
    class DoesNotExists(Exception):
        pass

    @classmethod
    async def create(cls, **kwargs) -> T:
        """
        # Создает новый объект и возвращает его.
        :param kwargs: Поля и значения для объекта.
        :return: Созданный объект.
        """

        async with async_db_session() as session:
            obj = cls(**kwargs)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @classmethod
    async def add(cls, **kwargs):
        """
        # Создает новый объект.
        :param kwargs: Поля и значения для объекта.
        """
        async with async_db_session() as session:
            obj = cls(**kwargs)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)  # важно — чтобы получить ID
            return obj

    async def update(obj, **kwargs) -> None:
        """
        # Обновляет текущий объект.
        :param kwargs: Поля и значения, которые надо поменять.
        """
        pk_column = obj.__class__.__mapper__.primary_key[0]
        pk_value = getattr(obj, pk_column.name)

        async with async_db_session() as session:
            await session.execute(
                sqlalchemy_update(obj.__class__)
                .where(pk_column == pk_value)
                .values(**kwargs)
            )
            await session.commit()

    async def delete(self) -> None:
        """
        # Удаляет объект.
        """
        async with async_db_session() as session:
            await session.delete(self)
            await session.commit()

    @classmethod
    async def get(cls, select_in_load: str | None = None, **kwargs) -> T:
        """
        # Возвращает одну запись, которая удовлетворяет введенным параметрам.

        :param select_in_load: Загрузить сразу связанную модель.
        :param kwargs: Поля и значения.
        :return: Объект или вызовет исключение DoesNotExists.
        """

        params = [getattr(cls, key) == val for key, val in kwargs.items()]
        query = select(cls).where(*params)

        if select_in_load:
            query.options(selectinload(getattr(cls, select_in_load)))

        try:
            async with async_db_session() as session:
                results = await session.execute(query)
                (result,) = results.one()
                return result
        except NoResultFound:
            return None

    @classmethod
    async def filter(cls, select_in_load: str | None = None, **kwargs) -> Sequence[T]:
        """
        # Возвращает все записи, которые удовлетворяют фильтру.

        :param select_in_load: Загрузить сразу связанную модель.
        :param kwargs: Поля и значения.
        :return: Перечень записей.
        """

        params = [getattr(cls, key) == val for key, val in kwargs.items()]
        query = select(cls).where(*params)

        if select_in_load:
            query.options(selectinload(getattr(cls, select_in_load)))

        try:
            async with async_db_session() as session:
                results = await session.execute(query)
                return results.scalars().all()
        except NoResultFound:
            return ()

    @classmethod
    async def all(
            cls, select_in_load: str = None, values: list[str] = None
    ) -> Sequence[T]:
        """
        # Получает все записи.

        :param select_in_load: Загрузить сразу связанную модель.
        :param values: Список полей, которые надо вернуть, если нет, то все (default None).
        """

        if values and isinstance(values, list):
            # Определенные поля
            values = [getattr(cls, val) for val in values if isinstance(val, str)]
            query = select(cls).options(load_only(*values))
        else:
            # Все поля
            query = select(cls)

        if select_in_load:
            query.options(selectinload(getattr(cls, select_in_load)))

        async with async_db_session() as session:
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def exclude(cls, select_in_load: str | None = None, **kwargs) -> Sequence[T]:
        """
        Возвращает записи, которые не соответствуют фильтрам (исключает значения).
        :param select_in_load: Загрузить сразу связанную модель.
        :param kwargs: Поля и значения для исключения.
                    Если значение — список или кортеж, исключает все из этого списка.
        :return: Перечень записей.
        """
        conditions = []
        for key, val in kwargs.items():
            column = getattr(cls, key)
            if isinstance(val, (list, tuple, set)):
                conditions.append(not_(column.in_(val)))
            else:
                conditions.append(column != val)

        query = select(cls).where(*conditions)

        if select_in_load:
            query = query.options(selectinload(getattr(cls, select_in_load)))

        async with async_db_session() as session:
            result = await session.execute(query)
            return result.scalars().all()


# Специализация
class Specializations(Base, ModelAdmin):

    __tablename__ = "specializations"

    id_specialization: Mapped[intpk]
    name: Mapped[str]

    doctors: Mapped[list["Doctors"]] = relationship(
        back_populates="specialization",
        cascade="all, delete-orphan"
    )


# Врачи
class Doctors(Base, ModelAdmin):

    __tablename__ = "doctors"

    id_doctor: Mapped[intpk]

    full_name: Mapped[str]

    specialization_id: Mapped[int] = mapped_column(
        ForeignKey("specializations.id_specialization", ondelete="CASCADE")
    )

    cabinet: Mapped[str | None]

    specialization: Mapped["Specializations"] = relationship(
        back_populates="doctors"
    )

    schedules: Mapped[list["Schedules"]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan"
    )

    appointments: Mapped[list["Appointments"]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan"
    )


# График врачей
class Schedules(Base, ModelAdmin):

    __tablename__ = "schedules"

    id_schedule: Mapped[intpk]

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id_doctor", ondelete="CASCADE")
    )

    day_of_week: Mapped[str]

    start_time: Mapped[time]

    end_time: Mapped[time]

    doctor: Mapped["Doctors"] = relationship(
        back_populates="schedules"
    )


# Пациенты
class Patients(Base, ModelAdmin):

    __tablename__ = "patients"

    id_patient: Mapped[intpk]

    full_name: Mapped[str]

    address: Mapped[str]

    birth_date: Mapped[date | None]

    phone: Mapped[str | None]

    appointments: Mapped[list["Appointments"]] = relationship(
        back_populates="patient",
        cascade="all, delete-orphan"
    )


# Приёмы
class Appointments(Base, ModelAdmin):

    __tablename__ = "appointments"

    id_appointment: Mapped[intpk]

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id_patient", ondelete="CASCADE")
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id_doctor", ondelete="CASCADE")
    )

    appointment_date: Mapped[date]

    appointment_time: Mapped[time]

    diagnosis: Mapped[Optional[str]] = mapped_column(nullable=True)

    decision: Mapped[Optional[str]] = mapped_column(nullable=True, default='В ожидании приёма')

    patient: Mapped["Patients"] = relationship(
        back_populates="appointments"
    )

    doctor: Mapped["Doctors"] = relationship(
        back_populates="appointments"
    )