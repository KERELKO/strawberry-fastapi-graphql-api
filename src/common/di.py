from typing import AsyncGenerator
from dishka import Provider, provide, Scope

from src.common.db.sqlalchemy.config import Database
from src.products.graphql.resolvers.products import StrawberryProductResolver
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.users.graphql.resolver import StrawberryUserResolver

from src.products.repositories.base import (
    AbstractReviewRepository,
    AbstractProductRepository,
)
from src.products.repositories.sqlalchemy.products.repo import (
    SQLAlchemyAggregatedProductRepository,
)
from src.products.repositories.sqlalchemy.reviews.repo import (
    SQLAlchemyAggregatedReviewRepository,
)
from src.users.repositories.base import AbstractUserRepository
from src.users.repositories.sqlalchemy.repo import (
    SQLAlchemyAggregatedUserRepository,
)


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
