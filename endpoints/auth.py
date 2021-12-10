from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from core.security import create_access_token
from core.security import verify_password
from endpoints.depends import get_user_repository
from models.token import Login
from models.token import Token
from repositories.users import UserRepository

router = APIRouter()


@router.post("/", response_model=Token)
async def login(login: Login, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(login.email)
    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username of password",
        )
    return Token(
        access_token=create_access_token({"sub": user.email}), token_type="Bearer"
    )
