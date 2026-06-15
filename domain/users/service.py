from domain.users.dto import CreateUserDTO, UserWithPasswordDTO
from domain.users.models import User


class UserService:
    async def get_user_by_email(self, email: str) -> User:
        """Получить пользователя по адресу электронной почты.

        :param email: Адрес электронной почты пользователя
        :return: Объект модели пользователя
        :raises UserNotFoundError: Если пользователь с указанным email не существует
        """
        raise NotImplementedError

    async def get_user_by_id(self, id: int) -> User:
        """Получить пользователя по ID.

        :param id: Идентификатор пользователя
        :return: Объект модели пользователя
        :raises UserNotFoundError: Если пользователь с указанным ID не существует
        """
        raise NotImplementedError

    async def create_user(self, user: CreateUserDTO) -> User:
        """Создать нового пользователя.

        :param user: Объект передачи данных для создания пользователя
        :return: Созданный объект модели пользователя
        :raises UserAlreadyExistsError: Если пользователь с указанным email уже существует
        """
        raise NotImplementedError

    async def update_user(self, user: UserWithPasswordDTO) -> User:
        """Обновить существующего пользователя.

        :param user: Объект передачи данных пользователя с паролем
        :return: Обновленный объект модели пользователя
        :raises UserNotFoundError: Если пользователь с указанным email не существует
        """
        raise NotImplementedError
