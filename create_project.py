import random
import csv
import sys

from sqlalchemy import create_engine, schema
from sqlalchemy.orm.session import sessionmaker

from database.elector import Elector
from database.prepared_token import Prepared_Token
from database.connector import dbconnect

engine = dbconnect()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

elect=[]

session.query(Elector).delete()
session.query(Prepared_Token).delete()
session.commit()

with open(sys.argv[2], 'r') as f:
    electors = []

    for row in csv.reader(f):
        session.add(Elector(
            student_id = row[1],
            name = row[2],
            department = row[3],
            card_id = row[0],
            project_id = sys.argv[1]
        ))

    session.commit()

print('Elector done')

prepared_tokens = random.sample(range(0,100000),99999)

for token in prepared_tokens:
    session.add(Prepared_Token(
        token = "{:0>5}".format(token),
        project_id = sys.argv[1]
    ))

session.commit()

print('Prepared Token done')

session.close()
engine.dispose()