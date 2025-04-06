from dataclasses import dataclass, field

import strawberry
from strawberry.types.nodes import Selection

from src.api.graphql.v1.converters.user import StrawberryUserConverter
from src.api.graphql.v1.mutations.inputs import UpdateUserInput, UserInput
from src.api.graphql.v1.queries.user import User
from src.core.dto import SelectedFields, UserDTO
from src.gateways.base import UserGateway

from .base import BaseStrawberryResolver


@dataclass(eq=False, repr=False, slots=True)
class StrawberryUserResolver(BaseStrawberryResolver):
    gw: UserGateway
    converter: StrawberryUserConverter = field(default_factory=StrawberryUserConverter)

    async def get_list(
        self,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
    ) -> list[User]:
        required_fields: list[SelectedFields] = self._selections_to_selected_fields(fields=fields)
        users = await self.gw.get_list(fields=required_fields, offset=offset, limit=limit)
        return [self.converter.convert(user) for user in users]

    async def get(
        self,
        id: strawberry.ID,
        fields: list[Selection],
    ) -> User | None:
        required_fields = self._selections_to_selected_fields(fields=fields)
        user = await self.gw.get(id=int(id), fields=required_fields)
        return self.converter.convert(user) if user else None

    async def get_by_review_id(
        self,
        review_id: strawberry.ID,
        fields: list[Selection],
    ) -> User | None:
        required_fields = self._selections_to_selected_fields(fields=fields)
        user = await self.gw.get_by_review_id(
            review_id=int(review_id), fields=required_fields,
        )
        return self.converter.convert(user) if user else None

    async def create(self, input: UserInput) -> User:
        dto = UserDTO(**strawberry.asdict(input))  # type: ignore[arg-type]
        new_user = await self.gw.add(dto=dto)
        return User(**new_user.model_dump())

    async def update(self, id: strawberry.ID, input: UpdateUserInput) -> User | None:
        dto = UserDTO(**strawberry.asdict(input))  # type: ignore[arg-type]
        updated_user = await self.gw.update(id=int(id), dto=dto)
        return self.converter.convert(updated_user) if updated_user else None

    async def delete(self, id: strawberry.ID) -> bool:
        return await self.gw.delete(id=int(id))
