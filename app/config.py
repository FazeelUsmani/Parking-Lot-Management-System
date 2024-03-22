from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "mongodb://localhost:27017/"
    database_name: str = "parking_lot"
    parking_lot_size: int

    class Config:
        env_file = ".env"

settings = Settings()
