from pydantic import BaseModel
from typing import List


class Author(BaseModel):
    name: str
    books: List[str]
