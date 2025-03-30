from src.common.exceptions import ObjectDoesNotExistException
from src.common.base.dto import SelectedFields
from src.users.dto import UserDTO
from src.users.repositories.base import AbstractUserUnitOfWork


class UserService:
    def _get_uow(self) -> AbstractUserUnitOfWork:
        from src.common.di import Container
        uow: AbstractUserUnitOfWork = Container.resolve(AbstractUserUnitOfWork)
        return uow

    async def get_user_list(
        self,
        fields: list[SelectedFields],
        offset: int,
        limit: int,
    ) -> list[UserDTO]:
        uow = self._get_uow()
        async with uow:
            users: list[UserDTO] = await uow.users.get_list(
                fields=fields, offset=offset, limit=limit,
            )
            await uow.commit()
        return users

    async def get_user_by_id(
        self,
        id: int,
        fields: list[SelectedFields],
    ) -> UserDTO | None:
        uow = self._get_uow()
        async with uow:
            try:
                user: UserDTO | None = await uow.users.get(id=id, fields=fields)
            except ObjectDoesNotExistException:
                user = None
            await uow.commit()
        return user

    async def get_user_by_review_id(
        self,
        review_id: int,
        fields: list[SelectedFields],
    ) -> UserDTO | None:
        uow = self._get_uow()
        async with uow:
            try:
                user: UserDTO | None = await uow.users.get_by_review_id(
                    review_id=review_id, fields=fields,
                )
            except ObjectDoesNotExistException:
                user = None
            await uow.commit()
        return user

    async def create_user(self, dto: UserDTO) -> UserDTO:
        uow = self._get_uow()
        async with uow:
            new_user: UserDTO = await uow.users.create(dto=dto)
            await uow.commit()
        return new_user

    async def update_user(self, id: int, dto: UserDTO) -> UserDTO | None:
        uow = self._get_uow()
        async with uow:
            updated_user: UserDTO | None = await uow.users.update(dto=dto, id=id)
            await uow.commit()
        return updated_user

    async def delete_user(self, id: int) -> bool:
        uow = self._get_uow()
        async with uow:
            is_deleted = await uow.users.delete(id=id)
            await uow.commit()
        return is_deleted
