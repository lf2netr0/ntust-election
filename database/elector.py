from sqlalchemy import Column, INT, String
from . import base

class Elector(base.Base):
    __tablename__ = 'elector'

    id = Column(INT, primary_key = True)
    student_id = Column(String(10), nullable = False)
    name = Column(String(40), nullable = False)
    department = Column(String(20), nullable = False)
    card_id = Column(String(256), nullable = False)
    status = Column(INT, nullable = False, default = 0)
    project_id = Column(INT, nullable = False)
