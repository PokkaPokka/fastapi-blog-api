from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    SQLALCHEMY_DATABASE_URL: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    OAUTH_SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()