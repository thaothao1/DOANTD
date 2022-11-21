import uvicorn
from fastapi import FastAPI
from router.api import api
from fastapi.staticfiles import StaticFiles

app = FastAPI(debug= True)
app.include_router(api)

app.mount("/static", StaticFiles(directory="static"), name="static")
if __name__ == "__main__":

    uvicorn.run("main:app")



