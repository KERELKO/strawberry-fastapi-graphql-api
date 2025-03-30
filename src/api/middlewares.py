from pprint import pprint
from dishka import AsyncContainer
from dishka import Scope as DIScope
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.base import BaseHTTPMiddleware

from src.common.db.sqlalchemy.config import Database


class ContainerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, container: AsyncContainer) -> None:
        super().__init__(app)
        self.container = container
        self.db: Database | None = None

    async def dispatch(self, request, call_next):
        print(request.method, request.url)
        if request.method == 'POST':
            pprint(dict(await request.json()))
            db = self.db or await self.container.get(Database)
            async with db.async_session_factory() as session:
                context = {AsyncSession: session}
                async with request.app.state.dishka_container(
                    context,
                    scope=DIScope.REQUEST,
                ) as request_container:
                    request.state.dishka_container = request_container
                    response = await call_next(request)
            if session.is_active:
                await session.aclose()
                context.clear()
        else:
            response = await call_next(request)
        return response
