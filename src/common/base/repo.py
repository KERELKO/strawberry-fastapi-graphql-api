from abc import ABC
from typing import Generic, TypeVar

from src.common.base.dto import SelectedFields


T = TypeVar('T')


class AbstractRepository(Generic[T], ABC):
    async def get(self, id: int, fields: list[SelectedFields]) -> T:
        raise NotImplementedError

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[T]:
        raise NotImplementedError

    async def add(self, dto: T) -> T:
        raise NotImplementedError

    async def update(self, id: int, dto: T) -> T | None:
        raise NotImplementedError

    async def delete(self, id: int) -> bool:
        raise NotImplementedError
