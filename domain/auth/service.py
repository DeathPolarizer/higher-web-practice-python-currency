from domain.auth.dto import Token


class AuthService:
    ALGORITHM = "HS256"

    async def login(self, email: str, password: str) -> Token:
        """Аутентифицировать пользователя и создать токены.

        :param email: Адрес электронной почты пользователя
        :param password: Пароль в виде обычного текста
        :return: Объект токена с access и refresh токенами
        :raises CredentialsError: Если учетные данные недействительны
        """
        raise NotImplementedError

    async def refresh_tokens(self, refresh_token: str) -> Token:
        """Обновить access токен, используя refresh токен.

        :param refresh_token: Строка refresh токена
        :return: Новый объект токена с обновленными access и refresh токенами
        """
        raise NotImplementedError
