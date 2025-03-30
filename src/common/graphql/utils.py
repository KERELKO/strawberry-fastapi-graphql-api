import strawberry
from strawberry.types.nodes import Selection


def get_required_fields(info: strawberry.Info) -> list[Selection]:
    return [f.selections for f in info.selected_fields][0]
