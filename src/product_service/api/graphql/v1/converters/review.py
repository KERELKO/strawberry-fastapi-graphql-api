from product_service.core.dto import ReviewDTO, Entity
from product_service.api.graphql.v1.queries.review import Review


class StrawberryReviewConverter:
    @classmethod
    def convert(cls, dto: ReviewDTO) -> Review:
        from product_service.api.graphql.v1.queries.product import Product
        from product_service.api.graphql.v1.queries.user import User

        data = dto.model_dump()
        product_data = {}
        user_data = {}

        if 'user_id' in data:
            user_data['_user_id'] = data.pop('user_id')
        if 'product_id' in data:
            product_data['_product_id'] = data.pop('product_id')

        if Entity.USER in data:
            _user = User(**data.pop('user'))
            user_data['_user'] = _user
        if Entity.PRODUCT in data:
            _product = Product(**data.pop('product'))
            product_data['_product'] = _product

        return Review(**product_data, **user_data, **data)
