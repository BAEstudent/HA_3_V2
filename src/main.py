from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers
from database import User #, create_db_and_tables
from auth.schemas import UserCreate, UserRead #, UserUpdate
from auth.auth import auth_backend #, current_active_user, fastapi_users
from auth.manager import get_user_manager
import uuid
from links.router import router as links_router
import uvicorn

app = FastAPI()

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager, 
    [auth_backend]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(links_router)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", log_level="info")
