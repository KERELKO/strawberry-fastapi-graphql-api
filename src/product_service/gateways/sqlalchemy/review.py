from typing import Sequence

import sqlalchemy as sql
from sqlalchemy.orm import joinedload

from product_service.core.db.sqlalchemy.base import BaseSQLAlchemyGateway
from product_service.core.db.sqlalchemy.extensions import (
    models_to_join,
    raise_exc,
    sqlalchemy_crud,
)
from product_service.core.db.sqlalchemy.models import ReviewORM
from product_service.core.dto import SelectedFields, UserDTO, ProductDTO, ReviewDTO


@sqlalchemy_crud(query_executor=False, model=ReviewORM)
class SQLAlchemyReviewGateway(BaseSQLAlchemyGateway):
    def _construct_select_query(self, fields: list[SelectedFields], **queries) -> sql.Select:
        _fields = fields[0] if len(fields) > 0 else raise_exc(Exception('No fields'))
        fields_to_select = [getattr(ReviewORM, f) for f in _fields.fields]
        review_id = queries.get('id', None)
        product_id = queries.get('product_id', None)
        user_id = queries.get('user_id', None)
        offset = queries.get('offset', None)
        limit = queries.get('limit', None)
        stmt = sql.select(*fields_to_select)

        if review_id is not None:
            return stmt.where(ReviewORM.id == review_id)
        elif user_id is not None:
            stmt = stmt.where(ReviewORM.user_id == user_id)
        elif product_id is not None:
            stmt = stmt.where(ReviewORM.product_id == product_id)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        return stmt

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
        product_id: int | None = None,
        user_id: int | None = None,
    ) -> list[ReviewDTO]:
        list_values = await self._execute_query(
            fields=fields,
            offset=offset,
            limit=limit,
            product_id=product_id,
            user_id=user_id,
        )
        dto_list = []
        for values in list_values:
            data = {f: v for f, v in zip(fields[0].fields, values)}
            dto_list.append(ReviewDTO(**data))
        return dto_list


class SQLAlchemyAggregatedReviewGateway(SQLAlchemyReviewGateway):
    """
    Special repository that allows to `solve N+1 problem`
    when retrieve single or mutiple models from the database
    """

    def _construct_join_statement(
        self,
        stmt: sql.Select,
        join_user: bool,
        join_product: bool,
    ) -> sql.Select:
        if join_user:
            stmt = stmt.options(joinedload(ReviewORM.user))
        if join_product:
            stmt = stmt.options(joinedload(ReviewORM.product))
        return stmt

    async def _fetch_many_with_related(
        self,
        join_user: bool,
        join_product: bool,
        **filters,
    ) -> Sequence[ReviewORM]:
        offset = filters.get('offset', 0)
        limit = filters.get('limit', 20)
        user_id = filters.get('user_id', None)
        product_id = filters.get('product_id', None)
        stmt = self._construct_join_statement(
            sql.select(ReviewORM).offset(offset).limit(limit), join_user, join_product,
        )
        if user_id is not None:
            stmt = stmt.where(ReviewORM.user_id == user_id)
        if product_id is not None:
            stmt = stmt.where(ReviewORM.product_id == product_id)

        reviews = await self.session.execute(stmt)
        return reviews.scalars().all()

    async def _fetch_one_with_related(
        self,
        join_user: bool = False,
        join_product: bool = False,
        **filters,
    ) -> ReviewORM | None:
        review_id = filters.get('id', None)
        stmt = self._construct_join_statement(sql.select(ReviewORM), join_user, join_product)
        if review_id is not None:
            stmt = stmt.where(ReviewORM.id == review_id)
        review = await self.session.execute(stmt)
        return review.scalar_one_or_none()

    async def get(self, id: int, fields: list[SelectedFields]) -> ReviewDTO | None:
        join_user, join_product, _ = models_to_join(fields)
        _review = await self._fetch_one_with_related(
            join_product=join_product, join_user=join_user, id=id,
        )
        if not _review:
            return None
        review = ReviewDTO(**_review.as_dict())
        if join_product:
            product = ProductDTO(**_review.product.as_dict())
            review.product = product  # type: ignore
        if join_user:
            user = UserDTO(**_review.user.as_dict())
            review.user = user  # type: ignore
        return review

    async def get_list(
        self,
        fields: list[SelectedFields],
        offset: int = 0,
        limit: int = 20,
        product_id: int | None = None,
        user_id: int | None = None,
    ) -> list[ReviewDTO]:
        join_user, join_product, _ = models_to_join(fields)
        _reviews = await self._fetch_many_with_related(
            join_product=join_product,
            join_user=join_user,
            product_id=product_id,
            user_id=user_id,
            offset=offset,
            limit=limit,
        )
        reviews: list[ReviewDTO] = []
        for _review in _reviews:
            review = ReviewDTO(**_review.as_dict())
            if join_product:
                product = ProductDTO(**_review.product.as_dict())
                review.product = product  # type: ignore
            if join_user:
                user = UserDTO(**_review.user.as_dict())
                review.user = user  # type: ignore
            reviews.append(review)
        return reviews
