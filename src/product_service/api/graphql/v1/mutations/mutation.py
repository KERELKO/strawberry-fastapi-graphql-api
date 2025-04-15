import strawberry

from .product import ProductMutations
from .review import ReviewMutations
from .user import UserMutations


@strawberry.type
class Mutation:
    @strawberry.field
    def users(self) -> UserMutations:
        return UserMutations()

    @strawberry.field
    def products(self) -> ProductMutations:
        return ProductMutations()

    @strawberry.field
    def reviews(self) -> ReviewMutations:
        return ReviewMutations()
