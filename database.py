from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://app_user:AppPassword123@localhost/crm"

engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine)
