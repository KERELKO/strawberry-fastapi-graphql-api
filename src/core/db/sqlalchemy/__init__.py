import asyncio

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core import logger
from src.core.settings import config

from .models import Base


class Database:
    def __init__(self) -> None:
        self.config = config
        self.engine = create_async_engine(config.postgres_connection_string)
        self.async_session_factory = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self.listen_for_events()

    def init(self):
        asyncio.run(self.create())

    async def create(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    def listen_for_events(self) -> None:
        if self.config.LISTEN_SQL_QUERIES:
            @event.listens_for(self.engine.sync_engine, 'before_execute')
            def sql_statement_listener(conn, clauseelement, multiparams, params):
                if config.DEBUG:
                    print(f'{'SQL stmt':-^40}\n{clauseelement}\n{'':-^40}')
                logger.info(f'SQL stmt: {clauseelement}')
