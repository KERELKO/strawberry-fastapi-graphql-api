from abc import abstractmethod
from src.products.dto import ProductDTO, ReviewDTO
from src.common.base.repo import AbstractRepository
from src.common.base.uow import AbstractUnitOfWork


class IProductRepository(AbstractRepository[ProductDTO]):
    @abstractmethod
    async def get_by_review_id(self, review_id: int, fields: list[str]) -> ProductDTO:
        ...


class IReviewRepository(AbstractRepository[ReviewDTO]):
    @abstractmethod
    async def get_list(
        self,
        fields: list[str],
        offset: int = 0,
        limit: int = 20,
        product_id: int | None = None,
        user_id: int | None = None,
    ) -> list[ReviewDTO]:
        ...


class AbstractProductUnitOfWork(AbstractUnitOfWork):
    products: IProductRepository


class AbstractReviewUnitOfWork(AbstractUnitOfWork):
    reviews: IReviewRepository
