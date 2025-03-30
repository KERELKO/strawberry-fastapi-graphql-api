import strawberry

from src.common.graphql.base.schemas import IReview
from src.common.exceptions import ObjectDoesNotExistException
from src.common.utils import get_container
from src.products.graphql.resolvers.reviews import StrawberryReviewResolver
from src.products.graphql.schemas.reviews.inputs import ReviewInput, UpdateReviewInput
from src.products.graphql.schemas.reviews.queries import DeletedReview


@strawberry.type
class ReviewMutations:
    @strawberry.mutation
    async def create_review(self, input: ReviewInput, info: strawberry.Info) -> IReview:
        container = get_container(info)
        resolver: StrawberryReviewResolver = await container.get(StrawberryReviewResolver)
        new_review = await resolver.create(input=input)
        return new_review

    @strawberry.mutation
    async def update_review(
        self, input: UpdateReviewInput, id: strawberry.ID, info: strawberry.Info,
    ) -> IReview:
        container = get_container(info)
        resolver: StrawberryReviewResolver = await container.get(StrawberryReviewResolver)
        updated_review = await resolver.update(input=input, id=id)
        return updated_review

    @strawberry.mutation
    async def delete_review(self, id: strawberry.ID, info: strawberry.Info) -> DeletedReview:
        container = get_container(info)
        resolver: StrawberryReviewResolver = await container.get(StrawberryReviewResolver)
        try:
            deleted: DeletedReview = await resolver.delete(id=id)
        except ObjectDoesNotExistException:
            deleted.message = 'Review was not deleted'
            return deleted
        return deleted
