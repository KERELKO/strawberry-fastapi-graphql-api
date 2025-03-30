import strawberry

from src.common.exceptions import ObjectDoesNotExistException
from src.common.graphql.base.schemas import IProduct
from src.common.utils import get_container
from src.products.graphql.resolvers.products import StrawberryProductResolver
from src.products.graphql.schemas.products.inputs import (ProductInput,
                                                          UpdateProductInput)
from src.products.graphql.schemas.products.queries import DeletedProduct


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
    ) -> IProduct | None:
        container = get_container(info)
        resolver = await container.get(StrawberryProductResolver)
        updated_product = await resolver.update(input=input, id=id)
        return updated_product

    @strawberry.mutation
    async def delete_product(self, id: strawberry.ID, info: strawberry.Info) -> DeletedProduct:
        container = get_container(info)
        resolver = await container.get(StrawberryProductResolver)
        try:
            deleted = await resolver.delete(id=id)
        except ObjectDoesNotExistException:
            deleted.message = 'Product with given ID is not found'
            return deleted
        return deleted
