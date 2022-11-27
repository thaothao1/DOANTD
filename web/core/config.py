import os
import pathlib
from tkinter  import FIRST
from pydantic import AnyHttpUrl , BaseSettings , validator
from typing import List  , Optional , Union

ROOT = pathlib.Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    API_V1_STR : str = "/api"
    DEBUG = os.environ.get("DEBUG",True)
    APP_NAME = os.environ.get("APP_NAME","webcompaser")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY","dab99f4793ee51e1757d705cf73562d48b6783442994b7657b5b72865b93c1e7")
    JWT_TOKEN_EXPIRES_MINUTES = int(os.environ.get("JWT_TOKEN_EXPIRES_MINUTES",30))
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:postgres@postgres/postgres"

    class Config:
        case_sensitive = True

def get_settings():
    return Settings()

settings = get_settings()




        

