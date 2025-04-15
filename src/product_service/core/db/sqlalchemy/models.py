from typing import Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    ...


class UserORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    reviews: Mapped[list['ReviewORM']] = relationship(
        back_populates='user', cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return f'UserORM(id={self.id}, username={self.username})'

    def as_dict(self) -> dict[str, Any]:
        data = {
            'username': self.username,
            'id': self.id,
        }
        return data


class ReviewORM(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['UserORM'] = relationship()

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product: Mapped['ProductORM'] = relationship()

    def __repr__(self) -> str:
        return (
            f'ReviewORM(id={self.id}, content={self.content}, '
            f'user_id={self.user_id}, product_id={self.product_id})'
        )

    def as_dict(self) -> dict[str, Any]:
        data = {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'product_id': self.product_id,
        }
        return data


class ProductORM(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column()
    reviews: Mapped[list['ReviewORM']] = relationship(
        back_populates='product', cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return f'ProductORM(id={self.id}, title={self.title}, description={self.description})'

    def as_dict(self) -> dict[str, Any]:
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }
        return data
