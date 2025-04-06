import strawberry

from src.api.graphql.v1.interfaces import IDeleted, IProduct, IUpdated
from src.api.graphql.v1.mutations.inputs import (ProductInput,
                                                 UpdateProductInput)
from src.api.graphql.v1.resolvers.product import StrawberryProductResolver
from src.api.graphql.v1.utils import get_container
from src.core.exceptions import ObjectDoesNotExistException


@strawberry.type
class ProductMutations:
    @strawberry.mutation
    async def create_product(self, input: ProductInput, info: strawberry.Info) -> IProduct:
        container = get_container(info)
        resolver = await container.get(StrawberryProductResolver)
        new_product = await resolver.create(input=input)
        return new_product

    @strawberry.mutation
    async def update_product(
        self, id: strawberry.ID, input: UpdateProductInput, info: strawberry.Info,
    ) -> IUpdated:
        container = get_container(info)
        resolver = await container.get(StrawberryProductResolver)
        updated_product = await resolver.update(input=input, id=id)
        if updated_product is None:
            return IUpdated(message='Product not found', success=False)
        return IUpdated(success=True, message='OK')

    @strawberry.mutation
    async def delete_product(self, id: strawberry.ID, info: strawberry.Info) -> IDeleted:
        container = get_container(info)
        resolver = await container.get(StrawberryProductResolver)
        response = IDeleted(success=True)
        try:
            await resolver.delete(id=id)
        except ObjectDoesNotExistException:
            response.success = False
        return response
