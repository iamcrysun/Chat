import uuid

from fastapi import APIRouter, HTTPException, Depends, Cookie
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from server.models.user import User
from server.schemas.auth import SignInSchema, SignUpSchema
from server.utils.auth import authenticate_user
from server.utils.crypt import get_password_hash
from server.utils.db import get_db, sessions

templates = Jinja2Templates(directory="D:/Chat/web/view")

router = APIRouter(prefix='/auth')


@router.get('/sign-up/form')
async def sign_up_form(request: Request):
    return templates.TemplateResponse('reg.html', {"request": request})


@router.get('/sign-in/form')
async def sign_in_form(request: Request):
    return templates.TemplateResponse('auth.html', {"request": request})


@router.post("/sign-up/")
async def sign_up(registration_data: SignUpSchema,
                  db: Session = Depends(get_db)):
    """
    Registration (creation of a new user).
    Login immediately.
    """
    potentially_existing_user = db.query(User).filter(User.email == registration_data.email).first()

    if potentially_existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"detail": "User with the same email address or account name already exists"}
        )

    user = User(
        email=registration_data.email,
        password=get_password_hash(registration_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return await sign_in(
        SignInSchema(
            email=user.email,
            password=registration_data.password
        ),
        db
    )


@router.post("/sign-in/")
async def sign_in(login_data: SignInSchema,
                  db: Session = Depends(get_db)):
    user: User | None = await authenticate_user(login_data.email, login_data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"detail": "Incorrect account name or password"}
        )

    session_id = str(uuid.uuid4())
    sessions[session_id] = user.id

    response = JSONResponse({"detail": "Logged in successfully"})
    response.set_cookie("session", session_id, max_age=3600)
    print(sessions)
    return response


@router.post('/sign-out/')
async def sign_out(session: str = Cookie()):
    """Deletes a user session."""

    if session in sessions:
        del sessions[session]

        response = JSONResponse({"detail": f"Session {session} was removed"})
        response.delete_cookie('session')

        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session} not found"
        )


async def get_current_user(session: str = Cookie(None),
                           db: Session = Depends(get_db)):
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session ID not provided"
        )

    user_id = sessions[session]
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The session has expired. Please re-login"
        )

    return db.query(User).filter(User.id == user_id).one()


@router.get('/me/')
async def me(current_user: User = Depends(get_current_user)):
    return current_user
