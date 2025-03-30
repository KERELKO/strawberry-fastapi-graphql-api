from typing import AsyncGenerator
from dishka import Provider, provide, Scope

from src.core.db.sqlalchemy import Database
from src.api.graphql.v1.resolvers.product import StrawberryProductResolver
from src.api.graphql.v1.resolvers.review import StrawberryReviewResolver
from src.api.graphql.v1.resolvers.user import StrawberryUserResolver

from src.repositories.base import (
    AbstractReviewRepository,
    AbstractProductRepository,
    AbstractUserRepository,
)
from src.repositories.sqlalchemy.product import SQLAlchemyAggregatedProductRepository
from src.repositories.sqlalchemy.review import SQLAlchemyAggregatedReviewRepository
from src.repositories.sqlalchemy.user import SQLAlchemyAggregatedUserRepository


class AppContainer(Provider):
    @provide(scope=Scope.APP)
    def database(self) -> Database:
        return Database()

    @provide(scope=Scope.REQUEST, cache=False)
    async def user_repository(
        self,
        db: Database,
    ) -> AsyncGenerator[AbstractUserRepository, None]:
        session = db.async_session_factory()
        async with session:
            yield SQLAlchemyAggregatedUserRepository(session)

    @provide(scope=Scope.REQUEST, cache=False)
    async def product_repository(
        self,
        db: Database,
    ) -> AsyncGenerator[AbstractProductRepository, None]:
        session = db.async_session_factory()
        async with session:
            yield SQLAlchemyAggregatedProductRepository(session)

    @provide(scope=Scope.REQUEST, cache=False)
    async def review_repository(
        self, db: Database,
    ) -> AsyncGenerator[AbstractReviewRepository, None]:
        session = db.async_session_factory()
        async with session:
            yield SQLAlchemyAggregatedReviewRepository(session)

    @provide(scope=Scope.REQUEST, cache=False)
    def strawberry_review_resolver(
        self, repository: AbstractReviewRepository,
    ) -> StrawberryReviewResolver:
        return StrawberryReviewResolver(repository)

    @provide(scope=Scope.REQUEST, cache=False)
    def strawberry_product_resolver(
        self, repository: AbstractProductRepository,
    ) -> StrawberryProductResolver:
        return StrawberryProductResolver(repository)

    @provide(scope=Scope.REQUEST, cache=False)
    def strawberry_user_resolver(
        self, repository: AbstractUserRepository,
    ) -> StrawberryUserResolver:
        return StrawberryUserResolver(repository)
