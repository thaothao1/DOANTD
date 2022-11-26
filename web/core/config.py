import os
import pathlib
from tkinter  import FIRST
from pydantic import AnyHttpUrl , BaseSettings , validator
from typing import List  , Optional , Union

ROOT = pathlib.Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    API_V1_STR : str = "api/v1"

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
    APP_NAME = "price"
    DATABASE_DB = "price"
    DATABASE_HOST = "postgres"
    DATABASE_PASSWORD = "postgres"
    DATABASE_USER = "postgres"
    # SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:postgres@postgres/price"
    SQLALCHEMY_DATABASE_URI =  f"postgresql://postgres:thaothao123@localhost:5432/ThaoDieu"

    class Config:
        case_sensitive = True

settings = Settings()



        

