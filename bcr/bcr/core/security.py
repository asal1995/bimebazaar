from fastapi import Depends, HTTPException, Header
from jose import JWTError, constants, jwt
from requests import Request
from starlette import status

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


def get_current_user(request: Request,
                     env: Settings = Depends(get_settings), ):
    if ('authorization' in request.headers or 'AUTHORIZATION' in
        request.headers or 'Authorization' in request.headers) and \
            len(request.headers['authorization'].split(' ')) == 2:
        token_type = request.headers['authorization'].split(' ')[0].upper()
        if token_type == 'BEARER':
            try:
                key = env.jwt_pub_key
                tkn = request.headers['authorization'].split(' ')[1]
                payload = jwt.decode(tkn, key, algorithms=[constants.ALGORITHMS.ES256, ])
                user_id: str = payload.get("user_id")
                if user_id is None:
                    raise credentials_exception
            except JWTError:
                raise credentials_exception
            return int(user_id)

        raise forbidden_exception
    raise forbidden_exception
