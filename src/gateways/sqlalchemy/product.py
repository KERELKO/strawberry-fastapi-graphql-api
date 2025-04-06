from typing import Any, Sequence

import sqlalchemy as sql
from sqlalchemy.orm import joinedload

from src.core.db.sqlalchemy.base import BaseSQLAlchemyGateway
from src.core.db.sqlalchemy.extensions import models_to_join, sqlalchemy_crud
from src.core.db.sqlalchemy.models import ProductORM, ReviewORM
from src.core.exceptions import ObjectDoesNotExistException
from src.core.utils import raise_exc
from src.core.dto import SelectedFields, ProductDTO, ReviewDTO


@sqlalchemy_crud(query_executor=False, model=ProductORM)
class SQLAlchemyProductGateway(BaseSQLAlchemyGateway):
    def _construct_select_query(
        self,
        fields: list[SelectedFields],
        **queries,
    ) -> sql.Select:
        product_id = queries.get('id', None)
        review_id = queries.get('review_id', None)
        _fields = fields[0] if len(fields) > 0 else raise_exc(Exception('No fields'))
        fields_to_select = [getattr(ProductORM, f) for f in _fields.fields]
        offset = queries.get('offset', None)
        limit = queries.get('limit', None)
        stmt = sql.select(*fields_to_select)

        if product_id is not None:
            stmt = stmt.where(ProductORM.id == product_id)
        elif review_id is not None:
            stmt = stmt.join(ReviewORM)
            stmt = stmt.where(ReviewORM.id == review_id)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        return stmt

    async def get_by_review_id(self, review_id: int, fields: list[SelectedFields]) -> ProductDTO:
        values = await self._execute_query(fields=fields, review_id=review_id, first=True)
        if not values:
            raise ObjectDoesNotExistException('ProductORM')
        data: dict[str, Any] = {f: v for f, v in zip(fields[0].fields, values)}
        return ProductDTO(**data)

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ProductDTO]:
        list_values = await self._execute_query(fields=fields, offset=offset, limit=limit)
        dto_list = []
        for values in list_values:
            data = {f: v for f, v in zip(fields[0].fields, values)}
            dto_list.append(ProductDTO(**data))
        return dto_list


class SQLAlchemyAggregatedProductGateway(SQLAlchemyProductGateway):
    async def _fetch_one_with_related(self, join_reviews: bool, **filters) -> ProductORM | None:
        product_id = filters.get('id', None)
        review_id = filters.get('review_id', None)
        stmt: sql.Select = sql.Select(ProductORM)
        if join_reviews:
            stmt = stmt.options(joinedload(ProductORM.reviews))
        if product_id is not None:
            stmt = stmt.where(ProductORM.id == product_id)
        elif review_id is not None:
            stmt = stmt.join(ProductORM.reviews)
            stmt = stmt.where(ReviewORM.id == review_id)
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def _fetch_many_with_related(self, join_reviews: bool, **filters) -> Sequence[ProductORM]:
        offset = filters.get('offset', 0)
        limit = filters.get('limit', 20)
        stmt: sql.Select = sql.Select(ProductORM).offset(offset).limit(limit)
        if join_reviews:
            stmt = stmt.options(joinedload(ProductORM.reviews))
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get(self, id: int, fields: list[SelectedFields]) -> ProductDTO:
        _, _, join_review = models_to_join(fields)
        _product = await self._fetch_one_with_related(id=id, join_reviews=join_review)
        if not _product:
            raise ObjectDoesNotExistException(ProductORM.__name__, object_id=id)
        product = ProductDTO(**_product.as_dict())
        if join_review:
            reviews = [ReviewDTO(**r.as_dict()) for r in _product.reviews]
            product.reviews = reviews  # type: ignore
        return product

    async def get_by_review_id(self, review_id: int, fields: list[SelectedFields]) -> ProductDTO:
        review = await self.session.get(ReviewORM, review_id)
        if not review:
            raise ObjectDoesNotExistException('ReviewORM', object_id=review_id)
        return await self.get(id=review.product_id, fields=fields)

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ProductDTO]:
        _, _, join_review = models_to_join(fields)
        _products = await self._fetch_many_with_related(
            offset=offset, limit=limit, join_reviews=join_review,
        )
        products: list[ProductDTO] = []
        for _product in _products:
            product = ProductDTO(**_product.as_dict())
            if join_review:
                reviews = [ReviewDTO(**r.as_dict()) for r in _product.reviews]
                product.reviews = reviews  # type: ignore
            products.append(product)
        return products
