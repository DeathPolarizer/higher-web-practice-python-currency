
from pydantic import BaseModel

class CreateUserDTO(BaseModel):
    # TODO: опишите модель тела запроса для получения запроса на создание пользователя
    pass


class UserDTO(BaseModel):
    # TODO: опишите модель тела ответа с данными пользователя без пароля
    pass


class UserWithPasswordDTO(UserDTO):
    # TODO: опишите модель тела ответа с данными пользователя с паролем
    pass
