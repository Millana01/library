from fastapi import Depends
from fastapi.params import Depends as DependsType
from sqlalchemy.orm import Session

from src.app.database.dependencies import get_db


class SessionMixin:
    __session: Session = Depends(get_db())

    def session(self) -> Session:
        if isinstance(self.__session, DependsType):
            return next(get_db())
        return self.__session
