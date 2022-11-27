import uvicorn
from fastapi import FastAPI
from core.config import settings
from router.api import api
from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()
# app.include_router(api)
def get_app() -> FastAPI:
    application = FastAPI(title=settings.APP_NAME)
    # middleware support for cors
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api, prefix=settings.API_V1_STR)
    return application

app = get_app()

if __name__ == "__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True)
