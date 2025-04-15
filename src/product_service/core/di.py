from typing import AsyncGenerator
from dishka import AnyOf, Provider, provide, Scope

from product_service.core.db.sqlalchemy import Database
from product_service.api.graphql.v1.resolvers.product import StrawberryProductResolver
from product_service.api.graphql.v1.resolvers.review import StrawberryReviewResolver
from product_service.api.graphql.v1.resolvers.user import StrawberryUserResolver

from product_service.gateways.base import (
    ReviewGateway,
    ProductGateway,
    UserGateway,
)
from product_service.gateways.sqlalchemy.product import SQLAlchemyAggregatedProductGateway
from product_service.gateways.sqlalchemy.review import SQLAlchemyAggregatedReviewGateway
from product_service.gateways.sqlalchemy.user import SQLAlchemyAggregatedUserGateway


class AppContainer(Provider):
    @provide(scope=Scope.APP)
    def database(self) -> Database:
        return Database()

    @provide(scope=Scope.REQUEST, cache=False)
    async def user_repository(
        self,
        db: Database,
    ) -> AnyOf[
        AsyncGenerator[UserGateway, None],
        AsyncGenerator[SQLAlchemyAggregatedUserGateway, None],
    ]:
        session = db.async_session_factory()
        async with session:
            yield SQLAlchemyAggregatedUserGateway(session)

    @provide(scope=Scope.REQUEST, cache=False)
    async def product_repository(
        self,
        db: Database,
    ) -> AnyOf[
        AsyncGenerator[ProductGateway, None],
        AsyncGenerator[SQLAlchemyAggregatedProductGateway, None],
    ]:
        session = db.async_session_factory()
        async with session:
            yield SQLAlchemyAggregatedProductGateway(session)

    @provide(scope=Scope.REQUEST, cache=False)
    async def review_repository(
        self, db: Database,
    ) -> AnyOf[
        AsyncGenerator[ReviewGateway, None],
        AsyncGenerator[SQLAlchemyAggregatedReviewGateway, None],
    ]:
        session = db.async_session_factory()
        async with session:
            yield SQLAlchemyAggregatedReviewGateway(session)

    @provide(scope=Scope.REQUEST, cache=False)
    def strawberry_review_resolver(
        self, repository: ReviewGateway,
    ) -> StrawberryReviewResolver:
        return StrawberryReviewResolver(repository)

    @provide(scope=Scope.REQUEST, cache=False)
    def strawberry_product_resolver(
        self, repository: ProductGateway,
    ) -> StrawberryProductResolver:
        return StrawberryProductResolver(repository)

    @provide(scope=Scope.REQUEST, cache=False)
    def strawberry_user_resolver(
        self, repository: UserGateway,
    ) -> StrawberryUserResolver:
        return StrawberryUserResolver(repository)
