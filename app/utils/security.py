from passlib.context import CryptContext
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
from utils.config import (
    JWT_EXPIRATION_TIME_MINUTES,
    JWT_ALGORITH,
    JWT_SECRET_KEY,
    JWT_EXPIRED_MSG,
    JWT_INVALID_MSG,
    JWT_WRONG_ROLE,
)
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import time
from utils.db_functions import db_check_token_user, db_check_jwt_username
from starlette.status import HTTP_401_UNAUTHORIZED


pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(e)
        return False


async def authenticate_user(user: JWTUser):
    """
    Authenticate username and password
    """
    potential_users = await db_check_token_user(user)
    is_valid = False
    for db_user in potential_users:
        if verify_password(user.password, db_user["password"]):
            is_valid = True

    if is_valid:
        user.role = "admin"
        return user

    return None


def create_jwt_token(user: JWTUser):
    """
    JWT token 생성
    """
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {"sub": user.username, "role": user.role, "exp": expiration}
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITH)

    return jwt_token


async def check_jwt_token(token: str = Depends(oauth_schema)):
    """
    JWT token이 맞는지 체크
    """
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITH)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            is_valid = await db_check_jwt_username(username)
            if is_valid:
                return final_checks(role)
            else:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail=JWT_INVALID_MSG
                )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=JWT_EXPIRED_MSG
            )
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


def final_checks(role: str):
    """
    관리자 권한을 갖고 있는지 체크한다.
    """
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=JWT_WRONG_ROLE)
