import strawberry
from dishka import AsyncContainer
from fastapi import Request
from strawberry.types.nodes import Selection


def get_required_fields(info: strawberry.Info) -> list[Selection]:
    return [f.selections for f in info.selected_fields][0]


def get_container(info: strawberry.Info) -> AsyncContainer:
    """Return Dishka async container from request"""
    request: Request = info.context['request']
    container = request.state.dishka_container
    return container
