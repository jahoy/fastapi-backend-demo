from pydantic import BaseModel, Schema
from models.author import Author
from utils.config import ISBN_DESCRIPTION


class Book(BaseModel):
    isbn: str = Schema(None, description=ISBN_DESCRIPTION)
    name: str
    author: Author
    year: int = Schema(None, gt=1900, lt=2100)
