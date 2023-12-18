from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class SignInSchema(BaseModel):
    email: EmailStr
    password: str


class SignUpSchema(BaseModel):
    email: EmailStr
    password: str
