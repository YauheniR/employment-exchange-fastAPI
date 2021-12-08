from db.base import engine
from db.base import metadata
from db.jobs import jobs
from db.users import users

metadata.create_all(bind=engine)
