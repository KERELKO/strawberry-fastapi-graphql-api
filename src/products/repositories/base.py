from abc import abstractmethod

from src.common.base.dto import SelectedFields
from src.products.dto import ProductDTO, ReviewDTO
from src.common.base.repo import AbstractRepository
from src.common.base.uow import AbstractUnitOfWork


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


class AbstractProductUnitOfWork(AbstractUnitOfWork):
    products: AbstractProductRepository


class AbstractReviewUnitOfWork(AbstractUnitOfWork):
    reviews: AbstractReviewRepository
