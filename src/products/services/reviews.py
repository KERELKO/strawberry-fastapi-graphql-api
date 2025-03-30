from src.common.exceptions import ObjectDoesNotExistException
from src.common.base.dto import SelectedFields
from src.products.dto import ReviewDTO
from src.products.repositories.base import AbstractReviewUnitOfWork


class ReviewService:
    def _get_uow(self) -> AbstractReviewUnitOfWork:
        from src.common.di import AppContainer
        uow: AbstractReviewUnitOfWork = Container.resolve(AbstractReviewUnitOfWork)
        return uow

    async def get_review_by_id(self, id: int, fields: list[SelectedFields]) -> ReviewDTO | None:
        uow = self._get_uow()
        async with uow:
            try:
                review = await uow.reviews.get(id=id, fields=fields)
            except ObjectDoesNotExistException:
                review = None
            await uow.commit()
        return review

    async def get_review_list(
        self,
        fields: list[SelectedFields],
        offset: int,
        limit: int,
        user_id: int | None = None,
        product_id: int | None = None,
    ) -> list[ReviewDTO]:
        uow = self._get_uow()
        async with uow:
            reviews = await uow.reviews.get_list(
                fields=fields,
                offset=offset,
                limit=limit,
                user_id=user_id,
                product_id=product_id,
            )
            await uow.commit()
        return reviews

    async def create_review(self, dto: ReviewDTO) -> ReviewDTO:
        uow = self._get_uow()
        async with uow:
            new_review: ReviewDTO = await uow.reviews.create(dto=dto)
            await uow.commit()
        return new_review

    async def update_review(self, id: int, dto: ReviewDTO) -> ReviewDTO | None:
        uow = self._get_uow()
        async with uow:
            try:
                updated_review: ReviewDTO | None = await uow.reviews.update(dto=dto, id=id)
            except ObjectDoesNotExistException:
                updated_review = None
            await uow.commit()
        return updated_review

    async def delete_review(self, id: int) -> bool:
        uow = self._get_uow()
        async with uow:
            is_deleted = await uow.reviews.delete(id=id)
            await uow.commit()
        return is_deleted
