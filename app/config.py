from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    test: bool
    api_name: "Book Recommender"

settings = Settings()