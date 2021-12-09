from typing import List

from fastapi import APIRouter
from fastapi import Depends

from endpoints.depends import get_user_repository
from models.user import UserGet
from models.user import UserIn
from repositories.users import UserRepository

router = APIRouter()


@router.get("/", response_model=List[UserGet])
async def read_users(
    users: UserRepository = Depends(get_user_repository),
    limit: int = 100,
    skip: int = 0,
):
    return await users.get_all(limit=limit, skip=skip)


@router.post("/", response_model=UserGet)
async def create_user(
    user: UserIn, users: UserRepository = Depends(get_user_repository)
):
    return await users.create(u=user)


@router.put("/", response_model=UserGet)
async def update_user(
    id: int, user: UserIn, users: UserRepository = Depends(get_user_repository)
):
    return await users.update(id=id, u=user)
