from abc import abstractmethod
from typing import Any

import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession


class BaseSQLAlchemyGateway:
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
