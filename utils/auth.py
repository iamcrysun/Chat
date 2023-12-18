from pydantic import EmailStr

from models.user import User
from utils.crypt import crypt_context


async def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if user and await verify_password(password, user.password):
        return user
    return None
