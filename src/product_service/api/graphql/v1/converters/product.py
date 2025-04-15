from product_service.core.dto import ProductDTO
from product_service.api.graphql.v1.queries.product import Product

from .review import StrawberryReviewConverter


class StrawberryProductConverter:
    review_converter: type[StrawberryReviewConverter] = StrawberryReviewConverter

    @classmethod
    def convert(cls, dto: ProductDTO) -> Product:
        reviews = []
        data = dto.model_dump()
        if hasattr(dto, 'reviews'):
            reviews = [cls.review_converter.convert(p) for p in dto.reviews]
            data.pop('reviews')
        product = Product(**data, _reviews=reviews)
        return product
