import strawberry

from src.api.graphql.v1.interfaces import IDeleted, IReview
from src.api.graphql.v1.mutations.inputs import ReviewInput, UpdateReviewInput
from src.api.graphql.v1.resolvers.review import StrawberryReviewResolver
from src.api.graphql.v1.utils import get_container
from src.core.exceptions import ObjectDoesNotExistException


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
    async def delete_review(self, id: strawberry.ID, info: strawberry.Info) -> IDeleted:
        container = get_container(info)
        resolver: StrawberryReviewResolver = await container.get(StrawberryReviewResolver)
        try:
            deleted: IDeleted = await resolver.delete(id=id)
        except ObjectDoesNotExistException:
            deleted.message = 'Review was not deleted'
            return deleted
        return deleted
