from passlib.context import CryptContext
from models import User

# In-memory "database"
fake_db = {}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_user_by_username(username: str):
    return fake_db.get(username)

def create_user(username: str, password: str):
    hashed_password = get_password_hash(password)
    user = User(username=username, password=hashed_password)
    fake_db[username] = user
    return user

def get_all_users():
    return [{"username": user.username} for user in fake_db.values()]

