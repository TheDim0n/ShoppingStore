import importlib

from importlib import resources
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


from app.database.database import SessionLocal, engine
from app.database.crud import user
from app.dependencies import get_settings
from app.schemas.user import UserCreate
from app.utils import password as passwd
from app.utils.mock import write_mock_data


settings = get_settings()

app = FastAPI(root_path=settings.root_path, title="ShoppingStoreAPI")

# include all routers
plugins = [f.name[:-3] for f in resources.files("app.routers").iterdir()
           if f.name.endswith(".py") and f.name[0] != "_"]
for plugin in plugins:
    router = importlib.import_module(f"app.routers.{plugin}")
    app.include_router(router.router)


# setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[list(map(str.strip, settings.cors_origins.split(",")))],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.on_event("startup")
async def startup_event():
    with Session(engine) as db:
        db_init_user = user.get_user_by_login(db, settings.initial_user_username)
        if not db_init_user:
            new_user: UserCreate = UserCreate(
                login=settings.initial_user_username,
                password=passwd.hash(settings.initial_user_password)
            )
            user.create_user(db, new_user)

        if settings.load_mock:
            write_mock_data(db)
