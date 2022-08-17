from typing import List, TypeVar, Union

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import expression

from server.core.db import Base
from server.core.status_enum import StatusEnum

TableType = TypeVar("TableType", bound=Base)
CreateBaseSchema = TypeVar("CreateBaseSchema", bound=BaseModel)
UpdateBaseSchema = TypeVar("UpdateBaseSchema", bound=BaseModel)


class CRUDMixin:
    table: TableType = None  # type: ignore
    create_scheme: CreateBaseSchema = None  # type: ignore
    update_scheme: UpdateBaseSchema = None  # type: ignore

    @classmethod
    async def _execute_commit(cls, query: expression, session: AsyncSession):
        await session.execute(query)
        await session.commit()

    @classmethod
    async def create(cls, input_data: create_scheme, session: AsyncSession):
        """Create model"""
        obj = cls.table(**input_data.dict())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    def get_pk_attr(cls):
        """Get PK attribute of table"""
        return getattr(cls.table.__table__.c, cls.table.pk_name())

    @classmethod
    def _check_object(cls, obj: table) -> Union[bool, HTTPException]:
        """Check if object exist"""
        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")
        return True

    @classmethod
    async def list(cls, session: AsyncSession) -> table:
        """Get list of filtered objects"""
        query = select(cls.table).order_by(cls.table.id)
        objects = await session.execute(query)
        return objects.scalars().all()

    @classmethod
    async def retrieve(cls, pk: int, session: AsyncSession) -> Union[table, HTTPException]:
        """Get object by primary key"""
        query = select(cls.table).where(cls.get_pk_attr() == pk)
        res = await session.execute(query)
        obj = res.scalars().first()
        cls._check_object(obj)
        await session.refresh(obj)
        return obj

    @classmethod
    async def bulk_retrieve(cls, pks: List[int], session: AsyncSession) -> List[table] or HTTPException:
        """Get object by primary key"""
        query = select(cls.table).where(cls.get_pk_attr().in_(pks))
        res = await session.execute(query)
        objs = res.scalars().all()
        [cls._check_object(obj) for obj in objs]
        [await session.refresh(obj) for obj in objs]
        return objs

    @classmethod
    async def update(
        cls,
        pk: int,
        input_data: update_scheme,
        session: AsyncSession,
        partial: bool = False,
    ) -> Union[table, HTTPException]:
        """Update object by specified primary key"""
        retrieved_obj = await cls.retrieve(pk, session)
        query = update(cls.table).where(cls.get_pk_attr() == pk).values(**input_data.dict(exclude_unset=partial))
        await cls._execute_commit(query, session)
        return retrieved_obj

    @classmethod
    async def bulk_update(
        cls,
        pks: List[int],
        input_data: update_scheme,
        session: AsyncSession,
        partial: bool = False,
    ) -> List[table] or HTTPException:
        """Update object by specified primary key"""
        retrieved_objs = await cls.bulk_retrieve(pks, session)
        query = update(cls.table).where(cls.get_pk_attr().in_(pks)).values(**input_data.dict(exclude_unset=partial))
        await cls._execute_commit(query, session)
        return retrieved_objs

    @classmethod
    async def delete(cls, pk: int, session: AsyncSession) -> dict or HTTPException:
        """Delete object by specified primary key"""
        await cls.retrieve(pk, session)
        query = delete(cls.table).where(cls.get_pk_attr() == pk)
        await cls._execute_commit(query, session)
        return {"status": StatusEnum.success.value}

    @classmethod
    async def delete_all(cls, session: AsyncSession):
        query = delete(cls.table)
        await cls._execute_commit(query, session)
        return {"status": StatusEnum.success.value}

    @classmethod
    async def get_first_by_filter(cls, filters: dict, session: AsyncSession):
        query = select(cls.table).filter_by(**filters)
        res = await session.execute(query)
        return res.scalars().first()

    @classmethod
    async def get_last_by_filter(cls, filters: dict, session: AsyncSession):
        query = select(cls.table).filter_by(**filters).order_by(desc("id"))
        res = await session.execute(query)
        return res.scalars().first()

    @classmethod
    async def get_or_create(cls, input_data: create_scheme, session: AsyncSession):
        res = await cls.get_first_by_filter(input_data.dict(), session)
        if res:
            return res
        return await cls.create(input_data, session)

    @classmethod
    async def get_by_ids(cls, ids: [int], session: AsyncSession):
        query = select(
            [cls.table],
            cls.table.id.in_(ids),
        )
        res = await session.execute(query)
        return res.scalars().all()

    @classmethod
    async def update_with_dict(
        cls,
        pk: int,
        input_data: dict,
        session: AsyncSession,
    ) -> Union[table, HTTPException]:
        """Update object by specified primary key"""
        retrieved_obj = await cls.retrieve(pk, session)
        query = update(cls.table).where(cls.get_pk_attr() == pk).values(**input_data)
        await cls._execute_commit(query, session)
        return retrieved_obj
