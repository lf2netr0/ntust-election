import random
import csv
import sys

from sqlalchemy import create_engine, schema
from sqlalchemy.orm.session import sessionmaker

from helper.helper import decrypt
from database.token import Token
from database.connector import dbconnect

engine = dbconnect()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

print(decrypt(session.query(Token).filter(Token.token=='84730').first().owner)) 

session.close()
engine.dispose()