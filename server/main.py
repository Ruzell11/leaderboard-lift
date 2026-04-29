from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}