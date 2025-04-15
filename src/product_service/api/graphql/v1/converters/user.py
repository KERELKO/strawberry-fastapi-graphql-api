from product_service.api.graphql.v1.converters.review import StrawberryReviewConverter
from product_service.core.dto import UserDTO
from product_service.api.graphql.v1.queries.user import User


class StrawberryUserConverter:
    review_converter: type[StrawberryReviewConverter] = StrawberryReviewConverter

    @classmethod
    def convert(cls, dto: UserDTO) -> User:
        reviews = []
        data = dto.model_dump()
        if hasattr(dto, 'reviews'):
            reviews = [cls.review_converter.convert(p) for p in dto.reviews]
            data.pop('reviews')
        product = User(**data, _reviews=reviews)
        return product
