import enum
from functools import wraps
from typing import Optional, Union
from starlette import status
from fastapi import Depends, HTTPException, Header
from jose import JWTError, constants, jwt

from bcr.core.config import Settings, get_settings

role_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Operation not permitted",
    headers={"WWW-Authenticate": "Bearer"},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate request token",
    headers={"WWW-Authenticate": "Bearer"},
)


async def verify_key(x_service_key: str = Header(...), settings: Settings = Depends(get_settings)):
    if x_service_key != settings.service_key:
        raise HTTPException(status_code=403, detail="Unauthorized access to api")
    return x_service_key
