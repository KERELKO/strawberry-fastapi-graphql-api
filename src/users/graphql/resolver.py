from dataclasses import dataclass, field

import strawberry
from strawberry.types.nodes import Selection

from src.common.graphql.base.resolvers import BaseStrawberryResolver
from src.common.base.dto import SelectedFields
from src.users.graphql.converter import StrawberryUserConverter
from src.users.graphql.schemas.inputs import UserInput, UpdateUserInput
from src.users.graphql.schemas.queries import User
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserRepository


@dataclass(eq=False, repr=False, slots=True)
class StrawberryUserResolver(BaseStrawberryResolver):
    repository: AbstractUserRepository
    converter: StrawberryUserConverter = field(default_factory=StrawberryUserConverter)

    async def get_list(
        self,
        fields: list[Selection],
        offset: int = 0,
        limit: int = 20,
    ) -> list[User]:
        required_fields: list[SelectedFields] = self._selections_to_selected_fields(fields=fields)
        users = await self.repository.get_list(fields=required_fields, offset=offset, limit=limit)
        return [self.converter.convert(user) for user in users]

    async def get(
        self,
        id: strawberry.ID,
        fields: list[Selection],
    ) -> User | None:
        required_fields = self._selections_to_selected_fields(fields=fields)
        user = await self.repository.get(id=int(id), fields=required_fields)
        return self.converter.convert(user) if user else None

    async def get_by_review_id(
        self,
        review_id: strawberry.ID,
        fields: list[Selection],
    ) -> User | None:
        required_fields = self._selections_to_selected_fields(fields=fields)
        user = await self.repository.get_by_review_id(
            review_id=int(review_id), fields=required_fields,
        )
        return self.converter.convert(user) if user else None

    async def create(self, input: UserInput) -> User:
        dto = UserDTO(**strawberry.asdict(input))
        new_user = await self.repository.add(dto=dto)
        return User(**new_user.model_dump())

    async def update(self, id: strawberry.ID, input: UpdateUserInput) -> User | None:
        dto = UserDTO(**strawberry.asdict(input))
        updated_user = await self.repository.update(id=int(id), dto=dto)
        return self.converter.convert(updated_user) if updated_user else None

    async def delete(self, id: strawberry.ID) -> bool:
        return await self.repository.delete(id=int(id))
