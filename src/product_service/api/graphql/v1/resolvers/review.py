from dataclasses import dataclass

import strawberry
from strawberry.types.nodes import Selection

from product_service.api.graphql.v1.converters.review import StrawberryReviewConverter
from product_service.api.graphql.v1.interfaces import IDeleted
from product_service.api.graphql.v1.mutations.inputs import ReviewInput, UpdateReviewInput
from product_service.api.graphql.v1.queries.review import Review
from product_service.core.dto import CreateReviewDTO, ReviewDTO, SelectedFields
from product_service.core.exceptions import ObjectDoesNotExistException
from product_service.gateways.base import ReviewGateway

from .base import BaseStrawberryResolver


@dataclass(eq=False, repr=False)
class StrawberryReviewResolver(BaseStrawberryResolver):
    gw: ReviewGateway

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
        reviews = await self.gw.get_list(
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
            review = await self.gw.get(fields=required_fields, id=int(id))
        except ObjectDoesNotExistException:
            return None
        return StrawberryReviewConverter.convert(review) if review else None

    async def create(self, input: ReviewInput) -> Review:
        data = strawberry.asdict(input)
        data['user_id'] = int(data['user_id'])
        data['product_id'] = int(data['product_id'])

        dto = CreateReviewDTO(**data)
        new_review = await self.gw.add(dto=dto)

        data = new_review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')

        return Review(**data)

    async def update(self, id: strawberry.ID, input: UpdateReviewInput) -> Review | None:
        dto = ReviewDTO(**strawberry.asdict(input))
        try:
            review = await self.gw.update(id=int(id), dto=dto)
        except ObjectDoesNotExistException:
            return None
        data = review.model_dump()
        data['_product_id'] = data.pop('product_id')
        data['_user_id'] = data.pop('user_id')
        return Review(**data)

    async def delete(self, id: strawberry.ID) -> bool:
        try:
            deleted = await self.gw.delete(id=int(id))
        except ObjectDoesNotExistException:
            deleted = False
        return deleted
