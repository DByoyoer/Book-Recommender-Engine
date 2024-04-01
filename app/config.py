from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env")
    database_url: str
    test: bool = False
    echo_sql: bool = False
    api_name:str = "Book Recommender"

settings = Settings()