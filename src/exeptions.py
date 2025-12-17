class ProjectException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ProjectException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(ProjectException):
    detail = "Объект уже существует"


class AllRoomsAreBookedException(ProjectException):
    detail = "Все номера забронированы"


class UserExistsException(ProjectException):
    detail = "Пользователь уже существует"


