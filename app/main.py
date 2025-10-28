from fastapi import FastAPI
from app.routes.category import router as category_router

app: FastAPI = FastAPI()

@app.get("/")
async def read_root():
    return {"status": "ok"}

app.include_router(category_router)