from datetime import UTC, datetime, timedelta

import jwt
from jwt.exceptions import InvalidTokenError

from config import settings


class JwtService:
    def create_access_token(self, subject: str) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": subject,
            "iat": now,
            "exp": now + timedelta(minutes=settings.jwt_access_token_expire_minutes),
        }
        return jwt.encode(
            payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

    def decode_subject(self, token: str) -> str | None:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm],
            )
        except InvalidTokenError:
            return None

        subject = payload.get("sub")
        return subject if isinstance(subject, str) else None


jwt_service = JwtService()
