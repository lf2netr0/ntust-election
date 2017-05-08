from helper.helper import send_mail
from helper.helper import path

from config import config

from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, schema

from database.mail_tosend import mail_tosend
from database.connector import dbconnect
from database.base import Base

engine = dbconnect()

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

content=""
with open(path('mail.txt'),"r") as f:
    content = f.read()

mail_list = session.query(mail_tosend).first()

while mail_list != None:

    to = mail_list.student_id + config['school_mail']
    content_personal = content.format(student_id= mail_list.student_id ,datetime=str(mail_list.gettime))
    
    try:
        result = send_mail(to, config['url'], config['key'],content_personal)
    except Exception :
        raise

    if result.status_code != 200:
        print(result)
    else:
        session.query(mail_tosend).filter(mail_tosend.id == mail_list.id).delete(synchronize_session=False)

    mail_list = session.query(mail_tosend).first()

session.commit()

session.close()
engine.dispose()
print("mail_list is empty.")
    


