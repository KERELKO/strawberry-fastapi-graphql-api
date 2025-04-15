import strawberry


@strawberry.input
class ReviewInput:
    content: str
    user_id: strawberry.ID
    product_id: strawberry.ID


@strawberry.input
class UpdateReviewInput:
    content: str


@strawberry.input
class ProductInput:
    title: str
    description: str


@strawberry.input
class UpdateProductInput:
    title: str = ''
    description: str = ''


@strawberry.input
class UserInput:
    username: str


@strawberry.input
class UpdateUserInput:
    username: str
