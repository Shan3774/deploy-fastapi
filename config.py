from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str
    class Config:
        env_file = ".env"   # for local dev

settings = Settings()
