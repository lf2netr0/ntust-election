from sqlalchemy import Column, INT, CHAR
from . import base

class Prepared_Token(base.Base):
    __tablename__ = 'prepared_token'

    id = Column(INT, primary_key = True)
    project_id = Column(INT, nullable = False)
    token = Column(CHAR(5), nullable = False)
