from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass

DATABASE_URL = "mysql+pymysql://app_user:AppPassword123@localhost/crm"

engine = create_engine(DATABASE_URL, echo=True)

session = sessionmaker(bind=engine)

def get_session():
    return session()