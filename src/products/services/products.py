from src.common.exceptions import ObjectDoesNotExistException
from src.common.base.dto import SelectedFields
from src.products.dto import ProductDTO
from src.products.repositories.base import AbstractProductRepository


class ProductService:
    def __init__(self, repository: AbstractProductRepository):
        self.repository = repository

    async def get_product_by_id(self, id: int, fields: list[SelectedFields]) -> ProductDTO | None:
        try:
            product = await self.repository.get(fields=fields, id=id)
        except ObjectDoesNotExistException:
            return None
        return product

    async def get_products_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ProductDTO]:
        products = await self.repository.get_list(fields=fields, offset=offset, limit=limit)
        return products

    async def get_by_review_id(
        self,
        review_id: int,
        fields: list[SelectedFields],
    ) -> ProductDTO | None:
        try:
            product = await self.repository.get_by_review_id(
                fields=fields, review_id=review_id,
            )
        except ObjectDoesNotExistException:
            return None
        return product

    async def create_product(self, dto: ProductDTO) -> ProductDTO:
        new_product: ProductDTO = await self.repository.create(dto=dto)
        return new_product

    async def update_product(self, id: int, dto: ProductDTO) -> ProductDTO | None:
        try:
            updated_product: ProductDTO | None = await self.repository.update(dto=dto, id=id)
        except ObjectDoesNotExistException:
            return None
        return updated_product

    async def delete_product(self, id: int) -> bool:
        is_deleted = await self.repository.delete(id=id)
        return is_deleted
