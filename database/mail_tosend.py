
from sqlalchemy import Column, INT, String, DateTime
from . import base

class mail_tosend(base.Base):
    __tablename__ = 'mail_tosend'

    id = Column(INT, primary_key = True)
    student_id = Column(String(10), nullable = False)
    gettime = Column(DateTime)
