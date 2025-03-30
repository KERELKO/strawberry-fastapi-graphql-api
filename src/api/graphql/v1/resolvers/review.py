from dataclasses import dataclass

import strawberry
from strawberry.types.nodes import Selection

from src.api.graphql.v1.interfaces import IDeleted
from src.core.exceptions import ObjectDoesNotExistException
from .base import BaseStrawberryResolver
from src.core.dto import ReviewDTO, SelectedFields, CreateReviewDTO
from src.api.graphql.v1.mutations.inputs import ReviewInput, UpdateReviewInput
from src.api.graphql.v1.queries.review import Review
from src.api.graphql.v1.converters.review import StrawberryReviewConverter
from src.repositories.base import AbstractReviewRepository


@dataclass(eq=False, repr=False)
class StrawberryReviewResolver(BaseStrawberryResolver):
    repository: AbstractReviewRepository

    async def get_list(
        self,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
        user_id: strawberry.ID | None = None,
        product_id: strawberry.ID | None = None,
    ) -> list[Review]:
        required_fields: list[SelectedFields] = self._selections_to_selected_fields(
            fields, remove_related=False,
        )
        reviews = await self.repository.get_list(
            fields=required_fields,
            offset=offset,
            limit=limit,
            user_id=int(user_id) if user_id else None,
            product_id=int(product_id) if product_id else None,
        )
        return [StrawberryReviewConverter.convert(r) for r in reviews]

    async def get(self, id: strawberry.ID, fields: list[Selection]) -> Review | None:
        required_fields: list[SelectedFields] = self._selections_to_selected_fields(
            fields, remove_related=False,
        )
        try:
            review = await self.repository.get(fields=required_fields, id=int(id))
        except ObjectDoesNotExistException:
            return None
        return StrawberryReviewConverter.convert(review) if review else None

    async def create(self, input: ReviewInput) -> Review:
        data = strawberry.asdict(input)
        data['user_id'] = int(data['user_id'])
        data['product_id'] = int(data['product_id'])

        dto = CreateReviewDTO(**data)
        new_review = await self.repository.add(dto=dto)

        data = new_review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')

        return Review(**data)

    async def update(self, id: strawberry.ID, input: UpdateReviewInput) -> Review | None:
        dto = ReviewDTO(**strawberry.asdict(input))
        try:
            review = await self.repository.update_review(id=int(id), dto=dto)
        except ObjectDoesNotExistException:
            return None
        data = review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')
        return Review(**data)

    async def delete(self, id: strawberry.ID) -> IDeleted:
        is_deleted = await self.repository.delete_review(id=int(id))
        return IDeleted(success=is_deleted)
