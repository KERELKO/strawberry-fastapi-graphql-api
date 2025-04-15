from typing import Protocol

from product_service.core.dto import ProductDTO, ReviewDTO, SelectedFields, UserDTO


class UserGateway(Protocol):
    async def get_by_review_id(self, review_id: int, fields: list[SelectedFields]) -> UserDTO:
        ...

    async def get(self, id: int, fields: list[SelectedFields]) -> UserDTO:
        raise NotImplementedError

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[UserDTO]:
        raise NotImplementedError

    async def add(self, dto: UserDTO) -> UserDTO:
        raise NotImplementedError

    async def update(self, id: int, dto: UserDTO) -> UserDTO:
        raise NotImplementedError

    async def delete(self, id: int) -> bool:
        raise NotImplementedError


class ProductGateway(Protocol):
    async def get_by_review_id(
        self,
        review_id: int,
        fields: list[SelectedFields],
    ) -> ProductDTO | None:
        ...

    async def get(self, id: int, fields: list[SelectedFields]) -> ProductDTO:
        raise NotImplementedError

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ProductDTO]:
        raise NotImplementedError

    async def add(self, dto: ProductDTO) -> ProductDTO:
        raise NotImplementedError

    async def update(self, id: int, dto: ProductDTO) -> ProductDTO:
        raise NotImplementedError

    async def delete(self, id: int) -> bool:
        raise NotImplementedError


class ReviewGateway(Protocol):
    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
        product_id: int | None = None,
        user_id: int | None = None,
    ) -> list[ReviewDTO]:
        ...

    async def get(self, id: int, fields: list[SelectedFields]) -> ReviewDTO:
        raise NotImplementedError

    async def add(self, dto: ReviewDTO) -> ReviewDTO:
        raise NotImplementedError

    async def update(self, id: int, dto: ReviewDTO) -> ReviewDTO:
        raise NotImplementedError

    async def delete(self, id: int) -> bool:
        raise NotImplementedError
