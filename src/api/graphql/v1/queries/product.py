import strawberry

from src.api.graphql.v1.interfaces import IProduct
from src.api.graphql.v1.queries.review import Review
from src.api.graphql.v1.resolvers.review import StrawberryReviewResolver
from src.api.graphql.v1.utils import get_container, get_required_fields


@strawberry.type
class Product(IProduct):
    id: strawberry.ID
    title: str
    description: str
    _reviews: list[Review] = strawberry.field(
        default_factory=list,
        name='_reviews',
        description='Do not use this field for queries, use "reviews" instead',
    )

    @strawberry.field
    async def reviews(
        self,
        info: strawberry.Info,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Review]:
        container = get_container(info)
        resolver = await container.get(StrawberryReviewResolver)

        if self._reviews:
            return self._reviews
        if not self.id:
            return []
        fields = get_required_fields(info)
        reviews = await resolver.get_list(
            fields=fields, product_id=self.id, offset=offset, limit=limit,
        )
        return reviews
