from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from application.auth_facade import auth_facade
from config import settings
from models.auth import TokenResponse
from security.rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
@limiter.limit(settings.auth_rate_limit)
async def issue_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    access_token = auth_facade.authenticate(form_data.username, form_data.password)
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(access_token=access_token)
