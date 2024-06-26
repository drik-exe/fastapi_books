from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import EXPIRATION_TIME
from database import get_session
from users.auth import create_jwt_token, get_current_user
from users.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        username: str,
        password: str,
        email: str,
        session: AsyncSession = Depends(get_session)):
    hashed_password = pwd_context.hash(password)

    try:
        new_user = User(username=username, hashed_password=hashed_password, email=email)
        session.add(new_user)
        await session.commit()
        return {"user": new_user}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await session.close()


@router.post("/token")
async def authenticate_user(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)):
    username = form_data.username
    password = form_data.password

    try:
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await session.close()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    is_password_correct = pwd_context.verify(password, user.hashed_password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    jwt_token = create_jwt_token({"sub": user.username})
    token_expiration = EXPIRATION_TIME

    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        max_age=int(token_expiration.total_seconds()),
        expires=int(token_expiration.total_seconds()),
    )
    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get("/user/me")
def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/user/edit")
async def edit_user(
        username: str | None = None,
        password: str | None = None,
        email: str | None = None,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)):

    try:
        query = select(User).where(User.username == current_user.username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if username is not None:
            user.username = username

        if email is not None:
            user.email = email

        if password is not None:
            hashed_password = pwd_context.hash(password)
            user.hashed_password = hashed_password

        session.add(user)

        await session.commit()
        return {"user": user}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        await session.close()


