import jwt
from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.config import EXPIRATION_TIME, SECRET_KEY, ALGORITHM
from src.database import get_session
from fastapi.security import OAuth2PasswordBearer
from src.users.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError:
        return None


async def get_token_from_cookie(request: Request):
    jwt_token = request.cookies.get("access_token")
    if not jwt_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return jwt_token


async def get_current_user(token: str = Depends(get_token_from_cookie), session: AsyncSession = Depends(get_session)):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    # user = get_user(decoded_data["sub"])

    try:
        query = select(User).where(User.username == decoded_data["sub"])
        result = await session.execute(query)
        user = result.scalar_one()
    except Exception as e:
        print(e)
        return {"error": str(e)}
    finally:
        await session.close()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user