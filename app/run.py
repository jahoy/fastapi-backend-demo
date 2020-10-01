from fastapi import FastAPI, Depends, HTTPException
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from utils.security import check_jwt_token
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, create_jwt_token
from models.jwt_user import JWTUser
from utils.config import (
    TOKEN_DESCRIPTION,
    TOKEN_SUMMARY,
    REDIS_URL,
    TESTING,
    IS_PRODUCTION,
    REDIS_URL_PRODUCTION,
    TOKEN_INVALID_CREDENTIALS_MSG,
)
from utils.db_object import db
import utils.redis_object as re
import aioredis
from utils.redis_object import check_test_redis
import pickle


app = FastAPI(
    title="Bookstore API Documentation",
    description="It is book store api documentation to give information",
    version="1.0.0",
)

app.include_router(
    app_v1,
    prefix="/v1",
    dependencies=[Depends(check_jwt_token), Depends(check_test_redis)],
)
app.include_router(
    app_v2,
    prefix="/v2",
    dependencies=[Depends(check_jwt_token), Depends(check_test_redis)],
)

# api에 때릴 때 마다 항상 먼저 실행됨
@app.on_event("startup")
async def connect_db():
    if not TESTING:
        await db.connect()
        if IS_PRODUCTION:
            re.redis = await aioredis.create_redis_pool(REDIS_URL_PRODUCTION)
        else:
            re.redis = await aioredis.create_redis_pool(REDIS_URL)

# api를 때릴 때 마다 제일 마지막에 실행됨
@app.on_event("shutdown")
async def disconnect_db():
    if not TESTING:
        await db.disconnect()

        re.redis.close()
        await re.redis.wait_closed()


@app.get("/")
async def health_check():
    return {"OK"}


@app.post("/token", description=TOKEN_DESCRIPTION, summary=TOKEN_SUMMARY)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    access token을 생성함
    """
    redis_key = f"token:{form_data.username},{form_data.password}"
    user = await re.redis.get(redis_key)

    if not user:
        jwt_user_dict = {"username": form_data.username, "password": form_data.password}
        jwt_user = JWTUser(**jwt_user_dict)
        user = await authenticate_user(jwt_user)

        if user is None:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=TOKEN_INVALID_CREDENTIALS_MSG
            )

        await re.redis.set(redis_key, pickle.dumps(user))
    else:
        user = pickle.loads(user)

    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}


@app.middleware("http")
async def middleware(request: Request, call_next):
    # response실행 전
    start_time = datetime.utcnow()
    
    # api 동작부분
    response = await call_next(request)
    
    #response실행후
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response
