from contextlib import asynccontextmanager

from dishka import make_async_container

from product_service.core.db.sqlalchemy import Database
from product_service.core.di import AppContainer

BASE_GRAPHQL_URL = 'http://localhost:8000/graphql'


FILL_DB_QUERY = """
INSERT INTO users (username) VALUES ('admin')
INSERT INTO products (title, description) VALUES ('title', 'description')
INSERT INTO reviews (content, user_id, product_id) VALUES ('content', 1, 1)
"""

CLEAR_DB_QUERY = """
DELETE FROM users;
DELETE FROM products;
DELETE FROM reviews;
"""


@asynccontextmanager
async def fill_db():
    container = make_async_container(AppContainer())
    db = await container.get(Database)
    try:
        async with db.engine.begin() as conn:
            conn.execute(FILL_DB_QUERY)
    finally:
        ...
