class CredentialsError(Exception):
    """Error with credentials"""


class UserNotFoundError(Exception):
    """Error when user not found"""


class UserAlreadyExistsError(Exception):
    """Error when user already exists"""


class CurrencyNotFoundError(Exception):
    """Error when currency not found"""
