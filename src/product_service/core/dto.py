from dataclasses import dataclass, field
from enum import Enum

from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    model_config = ConfigDict(extra='allow')
    id: int | None = None


class Entity(str, Enum):
    USER: str = 'user'
    PRODUCT: str = 'product'
    REVIEW: str = 'review'


@dataclass(eq=False)
class SelectedFields:
    owner: Entity | str
    all: bool = False
    fields: list[str] = field(default_factory=list)


class UserDTO(BaseDTO):
    username: str = ''


class ReviewDTO(BaseDTO):
    content: str = ''


class CreateReviewDTO(BaseDTO):
    user_id: int
    product_id: int
    content: str


class ProductDTO(BaseDTO):
    title: str = ''
    description: str = ''
