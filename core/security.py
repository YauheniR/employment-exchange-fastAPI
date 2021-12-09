import datetime

from jose import jwt
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
    return jwt.encode(to_encode, SECTER_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        encode_jwt = jwt.decode(token, SECTER_KEY, algorithms=ALGORITHM)
    except jwt.JWSError:
        return None
    return encode_jwt
