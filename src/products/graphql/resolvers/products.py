from dataclasses import dataclass

import strawberry
from strawberry.types.nodes import Selection

from src.common.exceptions import ObjectDoesNotExistException
from src.common.graphql.base.resolvers import BaseStrawberryResolver
from src.products.dto import ProductDTO
from src.products.graphql.schemas.products.inputs import ProductInput, UpdateProductInput
from src.products.graphql.schemas.products.queries import DeletedProduct, Product
from src.products.repositories.base import AbstractProductRepository
from src.products.graphql.converters.products import StrawberryProductConverter


@dataclass(eq=False, repr=False, slots=True)
class StrawberryProductResolver(BaseStrawberryResolver):
    converter = StrawberryProductConverter
    repository: AbstractProductRepository

    async def get_list(
        self,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
    ) -> list[Product]:
        required_fields = self._selections_to_selected_fields(fields)
        products = await self.repository.get_list(
            fields=required_fields, offset=offset, limit=limit,
        )
        return [self.converter.convert(p) for p in products]

    async def get(self, id: strawberry.ID, fields: list[Selection]) -> Product | None:
        required_fields = self._selections_to_selected_fields(fields)
        try:
            product = await self.repository.get(id=int(id), fields=required_fields)
        except ObjectDoesNotExistException:
            return None
        return self.converter.convert(product)

    async def get_by_review_id(
        self,
        review_id: strawberry.ID,
        fields: list[Selection],
    ) -> Product | None:
        required_fields = self._selections_to_selected_fields(fields)
        try:
            product = await self.repository.get_by_review_id(
                review_id=int(review_id), fields=required_fields,
            )
        except ObjectDoesNotExistException:
            return None
        return self.converter.convert(product)

    async def create(self, input: ProductInput) -> Product:
        dto = ProductDTO(**strawberry.asdict(input))
        new_product = await self.repository.add(dto=dto)
        return self.converter.convert(new_product)

    async def update(self, id: strawberry.ID, input: UpdateProductInput) -> Product | None:
        dto = ProductDTO(**strawberry.asdict(input))
        try:
            updated_product = await self.repository.update_product(id=int(id), dto=dto)
        except ObjectDoesNotExistException:
            return None
        return self.converter.convert(updated_product)

    async def delete(self, id: strawberry.ID) -> DeletedProduct:
        is_deleted = await self.repository.delete(id=int(id))
        return DeletedProduct(success=is_deleted, id=int(id))
