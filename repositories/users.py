import datetime
from typing import List
from typing import Optional

from core.security import hashed_password
from db import users
from models.user import User
from models.user import UserIn
from repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id == id)
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserIn) -> User:
        user = User(
            name=u.name,
            hashed_password=hashed_password(u.password),
            email=u.email,
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**user.dict()}
        values.pop("id", None)

        query = users.insert().values(**values)
        user.id = await self.database.execute(query=query)
        return user

    async def update(self, id: int, u: UserIn) -> User:
        user = User(
            id=id,
            name=u.name,
            hashed_password=hashed_password(u.password),
            email=u.email,
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**user.dict()}
        values.pop("id", None)
        values.pop("created_at", None)

        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query=query)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)
