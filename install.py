
from sqlalchemy import create_engine

from database.connector import dbconnect
from database import elector,prepared_token, token, mail_tosend
from database.base import Base



engine = dbconnect()

Base.metadata.bind = engine
Base.metadata.drop_all()
Base.metadata.create_all()

engine.dispose()