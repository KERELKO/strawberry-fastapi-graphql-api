import strawberry

from src.api.graphql.v1.exceptions import IDNotProvidedException
from src.api.graphql.v1.interfaces import IProduct, IReview, IUser
from src.api.graphql.v1.utils import get_container


@strawberry.type
class Review(IReview):
    id: strawberry.ID
    content: str
    _user_id: strawberry.ID | None = strawberry.field(name='_userId', default=None)
    _product_id: strawberry.ID | None = strawberry.field(name='_productId', default=None)
    _product: IProduct | None = strawberry.field(
        default=None,
        name='_product',
        description='Do not use this field for queries, use "product" instead',
    )
    _user: IUser | None = strawberry.field(
        default=None,
        name='_user',
        description='Do not use this field for queries, use "user" instead',
    )

    @strawberry.field
    async def product(self, info: strawberry.Info) -> IProduct | None:
        from src.api.graphql.v1.resolvers.product import \
            StrawberryProductResolver
        container = get_container(info)
        resolver: StrawberryProductResolver = await container.get(StrawberryProductResolver)
        if self._product is not None:
            return self._product
        if self._product_id:
            product = await resolver.get(
                id=self._product_id, fields=info.selected_fields,
            )
        else:
            if not self.id:
                raise IDNotProvidedException('Hint: add field \'id\' to the query schema')
            product = await resolver.get_by_review_id(
                review_id=self.id, fields=info.selected_fields,
            )
        return product

    @strawberry.field
    async def user(self, info: strawberry.Info) -> IUser | None:
        from src.api.graphql.v1.resolvers.user import StrawberryUserResolver

        container = get_container(info)
        resolver: StrawberryUserResolver = await container.get(StrawberryUserResolver)
        if self._user is not None:
            return self._user
        if not self.id:
            raise IDNotProvidedException('Hint: add field \'id\' to the query schema')
        if self._user_id:
            user = await resolver.get(
                id=self._user_id, fields=info.selected_fields,
            )
        else:
            user = await resolver.get_by_review_id(
                review_id=self.id, fields=info.selected_fields,
            )
        return user
