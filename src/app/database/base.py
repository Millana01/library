from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import declarative_base, sessionmaker

from src.app.config import Config

engine = create_engine(
    Config.db_url.format(
        Config.db_user, Config.db_password, Config.db_host, Config.db_name
    )
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseModel: DeclarativeMeta = declarative_base()
