from sqlalchemy import create_engine
from config import config

def dbconnect():
    return create_engine('mysql+mysqlconnector://{username}:{password}@{address}/{dbname}?charset=utf8'.format(
         username=config['database']['username'],
         password=config['database']['password'],
         dbname=config['database']['dbname'],
         address=config['database']['address'],
    ))