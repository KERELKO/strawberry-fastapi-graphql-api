from dataclasses import dataclass


class ApplicationException(Exception):
    ...


@dataclass(eq=False)
class ObjectDoesNotExistException(ApplicationException):
    obj: str
    object_id: int | None = None

    def __str__(self) -> str:
        return f'{self.obj} not found' + f', id: {self.object_id}' if self.object_id else ''


@dataclass(eq=False)
class IDNotProvided(ApplicationException):
    custom_message: str | None = None

    def __str__(self) -> str:
        msg = 'ID for the object is not provided'
        if self.custom_message:
            msg = f'{msg}: {self.custom_message}'
        return msg
