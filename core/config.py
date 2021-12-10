from starlette.config import Config

config = Config(".env_dev")

DATABASE_URL = config("EE_DATABASE_URL", cast=str, default="")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
SECTER_KEY = config(
    "EE_SECRET_KEY",
    cast=str,
    default="59020b4331218a880c6f541152fb05ed935512dc3e25bf45a308d5b67d4b9594",
)
