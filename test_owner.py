import sys
from config import config
from helper.helper import decrypt
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, schema
from database.token import Token
from database.connector import dbconnect
from database.base import Base

engine = dbconnect()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

tokenholder = session.query(Token
	).filter(Token.token == sys.argv[2] ,Token.project_id == sys.argv[1]).first()

print(decrypt(tokenholder.owner))

session.commit()

session.close()
engine.dispose()