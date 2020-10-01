import os

JWT_SECRET_KEY = "c07e154e8067407c909be11132e7d1bcee77542afd6c26ba613e2ffd9c3375ea"
JWT_ALGORITH = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60 * 24 * 5

TOKEN_DESCRIPTION = (
    "It checks username and password, then returns JWT token."
)
TOKEN_SUMMARY = "It returns JWT token."

ISBN_DESCRIPTION = "It is ID for books"

DB_HOST = "localhost"
DB_HOST_PRODUCTION = "167.71.12.16"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_NAME = "bookstore"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DB_URL_PRODUCTION = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_PRODUCTION}/{DB_NAME}"
)

UPLOAD_PHOTO_APIKEY = "d394465f8ceddab5768cbdc533549c39"
UPLOAD_PHOTO_URL = f"https://api.imgbb.com/1/upload?key={UPLOAD_PHOTO_APIKEY}"

REDIS_URL = "redis://localhost"
REDIS_URL_PRODUCTION = "redis://167.71.12.16"


TESTING = False
IS_LOAD_TEST = False
IS_PRODUCTION = True if os.environ["PRODUCTION"] == "true" else False

TEST_DB_HOST = "localhost"
TEST_DB_USER = "test"
TEST_DB_PASSWORD = "test"
TEST_DB_NAME = "test"
TEST_DB_URL = (
    f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}/{TEST_DB_NAME}"
)


TEST_REDIS_URL = "redis://localhost"

JWT_EXPIRED_MSG = "JWT token is expired! Renew the JWT token!"
JWT_INVALID_MSG = "Invalid JWT token!"
TOKEN_INVALID_CREDENTIALS_MSG = "Invalid username, password match !"
JWT_WRONG_ROLE = "Unauthorized role!"
