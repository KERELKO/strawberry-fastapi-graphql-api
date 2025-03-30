import strawberry


@strawberry.interface
class IUser:
    id: strawberry.ID
    username: str


@strawberry.interface
class IReview:
    id: strawberry.ID
    content: str


@strawberry.interface
class IProduct:
    id: strawberry.ID
    title: str
    description: str


@strawberry.interface
class IDeleted:
    success: bool
