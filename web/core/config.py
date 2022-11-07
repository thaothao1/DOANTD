import os
import pathlib
from tkinter  import FIRST
from pydantic import AnyHttpUrl , BaseSettings , EmailStr , validator
from typing import List  , Optional , Union

ROOT = pathlib.Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    API_V1_STR : str = "api/v1"


    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY","dab99f4793ee51e1757d705cf73562d48b6783442994b7657b5b72865b93c1e7")
    JWT_TOKEN_EXPIRES_MINUTES = int(os.environ.get("JWT_TOKEN_EXPIRES_MINUTES",30))

    BACKEND_CORS_ORIGINS : List[AnyHttpUrl] =[]

    @validator("BACKEND_CORS_ORIGINS" , pre= True) 
    def assemble_cors_orgins(cls , v : Union[str , List[str]]) -> Union[List[str],str]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.plit(",")]
        elif isinstance(v,(list , str)):
            return v
        raise ValueError(v)

    HOST_WEBAPP = "localhost"
    PORT_WEBAPP = "8000"
    APP_NAME = "price_comparing"
    DATABASE_DB = "price_comparing"
    DATABASE_HOST = "localhost"
    DATABASE_PASSWORD = "thudieu2708"
    DATABASE_USER = "postgres"
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:thaothao123@localhost:5432/FastApiSS"

    class Config:
        case_sensitive = True

settings = Settings()



        

