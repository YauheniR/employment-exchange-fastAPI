import datetime

import jwt
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.config import ALGORITHM
from core.config import SECTER_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
    )
    return jwt.encode(to_encode, key=SECTER_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    encode_jwt = jwt.decode(token=token, key=SECTER_KEY, algorithms=ALGORITHM)
    return encode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, *args, **kwargs):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request=request)
        exp = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token"
        )
        if credentials:
            token = decode_access_token(credentials.credentials)
            if token is None:
                raise exp
            return credentials.credentials
        else:
            raise exp
