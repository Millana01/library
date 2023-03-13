class Config:
    # Token settings
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # Database settings
    db_url = "postgresql+psycopg2://{}:{}@{}/{}"
    db_user = "postgres"
    db_password = "postgres"
    db_host = "localhost"
    db_name = "library"
