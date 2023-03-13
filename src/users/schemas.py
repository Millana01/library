from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    username: Union[str, None] = None
    is_active: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str
