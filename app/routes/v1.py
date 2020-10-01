from fastapi import FastAPI, Body, Header, File, APIRouter
from models.user import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response
from utils.helper_functions import upload_image_to_server
from utils.db_functions import (
    db_insert_personel,
    db_check_personel,
    db_get_book_with_isbn,
    db_get_author,
    db_get_author_from_id,
    db_patch_author_name,
)
import utils.redis_object as re
import pickle

app_v1 = APIRouter()


@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=["User"])
async def post_user(user: User):
    await db_insert_personel(user)
    return {"result": "personel is created"}


@app_v1.post("/login", tags=["User"])
async def get_user_validation(username: str = Body(...), password: str = Body(...)):
    redis_key = f"{username},{password}"
    result = await re.redis.get(redis_key)

    # Redis 로부터 데이터 획득했을 경우
    if result:
        if result == "true":
            return {"is_valid (redis)": True}
        else:
            return {"is_valid (redis)": False}
    # Redis가 데이터가 없을 경우
    else:
        result = await db_check_personel(username, password)
        await re.redis.set(redis_key, str(result))

        return {"is_valid (db)": result}


@app_v1.get(
    "/book/{isbn}",
    response_model=Book,
    response_model_include=["name", "year"],
    tags=["Book"],
)
async def get_book_with_isbn(isbn: str):
    result = await re.redis.get(isbn)

    if result:
        result_book = pickle.loads(result)
        return result_book
    else:
        book = await db_get_book_with_isbn(isbn)
        author = await db_get_author(book["author"])
        author_obj = Author(**author)
        book["author"] = author_obj
        result_book = Book(**book)

        await re.redis.set(isbn, pickle.dumps(result_book))
        return result_book


@app_v1.get("/author/{id}/book", tags=["Book"])
async def get_authors_books(id: int, order: str = "asc"):
    author = await db_get_author_from_id(id)
    if author is not None:
        books = author["books"]
        if order == "asc":
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)

        return {"books": books}
    else:
        return {"result": "no author with corresponding id !"}


@app_v1.patch("/author/{id}/name")
async def patch_author_name(id: int, name: str = Body(..., embed=True)):
    await db_patch_author_name(id, name)
    return {"result": "name is updated"}


@app_v1.post("/user/author")
async def post_user_and_author(
    user: User, author: Author, bookstore_name: str = Body(..., embed=True)
):
    return {"user": user, "author": author, "bookstore_name": bookstore_name}


@app_v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    await upload_image_to_server(profile_photo)
    return {"file size": len(profile_photo)}
