from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings
from app.security.jwt import jwt_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def require_admin(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    subject = jwt_service.decode_subject(token)
    if subject != settings.admin_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return subject


CurrentAdmin = Annotated[str, Depends(require_admin)]
