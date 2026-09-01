import hmac

from config import settings
from security.jwt import jwt_service


class AuthFacade:
    """Public application boundary for the authentication use case."""

    def authenticate(self, username: str, password: str) -> str | None:
        valid_username = hmac.compare_digest(username, settings.admin_username)
        valid_password = hmac.compare_digest(password, settings.admin_password)

        if not (valid_username and valid_password):
            return None

        return jwt_service.create_access_token(subject=username)


auth_facade = AuthFacade()
