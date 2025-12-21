from fastapi import HTTPException


class ProjectException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ProjectException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class ObjectAlreadyExistsException(ProjectException):
    detail = "Объект уже существует"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь уже существует"


class AllRoomsAreBookedException(ProjectException):
    detail = "Все номера забронированы"


class IncorrectTokenException(ProjectException):
    detail = "Некорректный токен"


class IncorrectPasswordException(ProjectException):
    detail = "Неверный пароль"


class EmailNotRegisteredException(ProjectException):
    detail = "Пользователь с таким email не зарегестрирован"


class ProjectHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class RoomNotFoundHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "Номера не существует"


class HotelNotFoundHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "Отеля не существует"


class AllRoomsAreBookedHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "Все номера забронированы"


class UserAlreadyExistsHTTPException(ProjectHTTPException):
    status_code = 409
    detail = "Пользователь уже существует"


class IncorrectTokenHTTPException(ProjectException):
    status_code = 401
    detail = "Некорректный токен"


class IncorrectPasswordHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Неверный пароль"


class EmailNotRegisteredHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегестрирован"