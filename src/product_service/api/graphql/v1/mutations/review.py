import strawberry

from product_service.api.graphql.v1.interfaces import IDeleted, IReview, IUpdated
from product_service.api.graphql.v1.mutations.inputs import ReviewInput, UpdateReviewInput
from product_service.api.graphql.v1.resolvers.review import StrawberryReviewResolver
from product_service.api.graphql.v1.utils import get_container
from product_service.core.exceptions import ObjectDoesNotExistException


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
    ) -> IUpdated:
        container = get_container(info)
        resolver: StrawberryReviewResolver = await container.get(StrawberryReviewResolver)
        updated_review = await resolver.update(input=input, id=id)
        if updated_review is None:
            return IUpdated(success=False, message='Review not found')
        return IUpdated(success=True, message='OK')

    @strawberry.mutation
    async def delete_review(self, id: strawberry.ID, info: strawberry.Info) -> IDeleted:
        container = get_container(info)
        resolver: StrawberryReviewResolver = await container.get(StrawberryReviewResolver)
        response = IDeleted(success=True)
        try:
            await resolver.delete(id=id)
        except ObjectDoesNotExistException:
            response.success = False
        return response
