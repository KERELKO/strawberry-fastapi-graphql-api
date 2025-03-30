import strawberry

from src.api.graphql.v1.interfaces import IDeleted, IUser
from src.core.exceptions import ObjectDoesNotExistException
from src.api.graphql.v1.utils import get_container
from src.api.graphql.v1.resolvers.user import StrawberryUserResolver
from src.api.graphql.v1.mutations.inputs import UpdateUserInput, UserInput


@strawberry.type
class DeletedUser(IDeleted):
    id: strawberry.ID
    success: bool
    message: str | None = None


@strawberry.type
class UserMutations:
    @strawberry.mutation
    async def register_user(self, input: UserInput, info: strawberry.Info) -> IUser:
        container = get_container(info)
        resolver: StrawberryUserResolver = await container.get(StrawberryUserResolver)
        new_user = await resolver.create(input=input)
        return new_user

    @strawberry.mutation
    async def update_user(
        self, id: strawberry.ID, input: UpdateUserInput, info: strawberry.Info,
    ) -> IUser | None:
        container = get_container(info)
        resolver: StrawberryUserResolver = await container.get(StrawberryUserResolver)
        updated_user = await resolver.update(input=input, id=id)
        return updated_user

    @strawberry.mutation
    async def delete_user(self, id: strawberry.ID, info: strawberry.Info) -> DeletedUser:
        container = get_container(info)
        resolver: StrawberryUserResolver = await container.get(StrawberryUserResolver)
        not_deleted = DeletedUser(id=id, success=False, message='User was not deleted')
        try:
            is_deleted = await resolver.delete(id=id)
        except ObjectDoesNotExistException:
            return not_deleted
        if is_deleted:
            return DeletedUser(id=id, success=True, message='User was deleted successfully!')
        return not_deleted
