from abc import abstractmethod

from src.common.base.uow import AbstractUnitOfWork
from src.common.base.repo import AbstractRepository
from src.common.base.dto import SelectedFields
from src.users.dto import UserDTO


class AbstractUserRepository(AbstractRepository[UserDTO]):
    @abstractmethod
    async def get_by_review_id(self, review_id: int, fields: list[SelectedFields]) -> UserDTO:
        ...


class AbstractUserUnitOfWork(AbstractUnitOfWork):
    users: AbstractUserRepository
