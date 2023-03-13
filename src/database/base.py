import logging
from abc import abstractmethod
from contextlib import contextmanager

import psycopg2
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import Config
from src.helpers.singleton import Singleton

logger = logging.getLogger(__name__)

BaseModel: DeclarativeMeta = declarative_base()


class BaseDB:
    _session = None

    @property
    @abstractmethod
    def host(self) -> str:
        """Must be implemented by child classes"""

    @property
    @abstractmethod
    def database(self) -> str:
        """Must be implemented by child classes"""

    @property
    @abstractmethod
    def user(self) -> str:
        """Must be implemented by child classes"""

    @property
    @abstractmethod
    def password(self) -> str:
        """Must be implemented by child classes"""

    def create_engine(self) -> Engine:
        db_url = Config.db_url.format(
            self.user, self.password, self.host, self.database
        )
        engine = create_engine(db_url, echo=True)
        return engine

    def _new_session(self) -> sessionmaker:
        engine = self.create_engine()
        session = sessionmaker()
        session.configure(bind=engine, expire_on_commit=False)
        return session()

    def _get_session(self) -> sessionmaker:
        if not self._session:
            return self._new_session()
        return self._session  # type: ignore

    @contextmanager
    def create_session(self) -> sessionmaker:
        session = self._get_session()
        try:
            yield session
            session.commit()
        except psycopg2.Error as error:
            session.rollback()
            self._session = None
            logger.error("Error while get connection", error)
            raise
        finally:
            session.close()


class LibraryDB(BaseDB, metaclass=Singleton):
    host = Config.db_host
    database = Config.db_name
    user = Config.db_user
    password = Config.db_password
