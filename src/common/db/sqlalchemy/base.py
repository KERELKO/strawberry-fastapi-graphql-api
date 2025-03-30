from abc import abstractmethod
from types import TracebackType
from typing import Any

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.common.base.uow import AbstractUnitOfWork


class BaseSQLAlchemyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @abstractmethod
    def _construct_select_query(self, *args, **queries) -> sql.Select:
        """
        Implement the method to make "_execute_query" work,
        params can be overriden with specific ones
        """

    async def _execute_query(
        self,
        *args,
        first: bool = False,
        **kwargs,
    ) -> list[tuple[Any, ...]] | tuple[Any, ...]:
        stmt = self._construct_select_query(*args, **kwargs)
        result = await self.session.execute(stmt)
        if first:
            return result.first()  # type: ignore
        return result.all()  # type: ignore


class BaseSQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

    async def __aexit__(
        self,
        exception: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exception:
            await self.rollback()
        await self.session.close()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()
