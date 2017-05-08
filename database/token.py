from sqlalchemy import Column, INT, CHAR, BOOLEAN, BLOB
from . import base

class Token(base.Base):
    __tablename__ = 'token'

    token = Column(CHAR(5), primary_key = True, autoincrement = False)
    project_id = Column(INT, primary_key = True, autoincrement = False)
    owner = Column(BLOB, nullable = False)
    used = Column(BOOLEAN, nullable = False, default = False)
