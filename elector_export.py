import sys
from config import config
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, schema
from database.elector import Elector
from database.connector import dbconnect
from database.base import Base

engine = dbconnect()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

voted = session.query(Elector
	).filter(Elector.status == 1 ,Elector.project_id == sys.argv[1])
for row in voted:
	print(row.student_id)


session.close()
engine.dispose()