from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
from admin.core.config import config


def create_access_token(data: dict, env: config):

    key = env.jwt_pri_key
    expire = datetime.utcnow() + timedelta(minutes=15)  # default exp time
    data.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(data, key, 'ES256')
        return encoded_jwt
    except JWTError as e:
        print("Failed to encode JWT:", str(e))
        raise HTTPException(status_code=500, detail="Failed to create access token")


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, config.jwt_pub_key, algorithms=["ES256"])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
