import asyncio
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

import strawberry
from strawberry.fastapi import GraphQLRouter

from src.common.db.sqlalchemy.config import Database
from src.common.di import AppContainer
from src.common.graphql.query import Query
from src.common.graphql.mutations import Mutation
from src.common.settings import config


container = make_async_container(AppContainer())


def init_db():
    async def wrapper():
        db = await container.get(Database)
        await db.create()
    asyncio.run(wrapper())


def graphql_app_factory() -> GraphQLRouter:
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql: GraphQLRouter = GraphQLRouter(schema, context_getter=lambda: {'container': container})

    return graphql


def fastapi_app_factory() -> FastAPI:
    app = FastAPI(**config.app_config)
    app.include_router(graphql_app_factory(), prefix='/graphql')
    setup_dishka(container, app)
    return app
