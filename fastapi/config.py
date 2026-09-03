import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    app_name: str = "Secure Support Agent Lab"
    app_version: str = "0.1.0"

    # Academic requirement: the single admin credential is kept in code.
    # Replace this mechanism before any real deployment.
    admin_username: str = "admin"
    admin_password: str = "admin123"

    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_secret_key: str = os.getenv(
        "JWT_SECRET_KEY",
        "local-development-only-secret-change-before-deploying",
    )


settings = Settings()
