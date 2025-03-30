from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.core.dto import SelectedFields, UserDTO, ProductDTO, ReviewDTO

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


class AbstractUserRepository(AbstractRepository[UserDTO]):
    @abstractmethod
    async def get_by_review_id(self, review_id: int, fields: list[SelectedFields]) -> UserDTO:
        ...


class AbstractProductRepository(AbstractRepository[ProductDTO]):
    @abstractmethod
    async def get_by_review_id(
        self,
        review_id: int,
        fields: list[SelectedFields],
    ) -> ProductDTO | None:
        ...


class AbstractReviewRepository(AbstractRepository[ReviewDTO]):
    @abstractmethod
    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
        product_id: int | None = None,
        user_id: int | None = None,
    ) -> list[ReviewDTO]:
        ...
