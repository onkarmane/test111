from fastapi import FastAPI, HTTPException, status
from schemas import UserCreate, UserOut
from services import create_user, get_user_by_username, verify_password
from services import get_all_users  # Add to existing imports
# This is comment for 1
app = FastAPI()

@app.post("/register", response_model=UserOut)
def register(user: UserCreate):
    if get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = create_user(user.username, user.password)
    return {"username": new_user.username}

@app.post("/login")
def login(user: UserCreate):
    db_user = get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful"}


@app.get("/users", response_model=list[UserOut])
def list_users():
    return get_all_users()
