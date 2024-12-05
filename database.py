import sentry_sdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


DATABASE_URL = "mysql+pymysql://app_user:AppPassword123@localhost/crm"

sentry_sdk.init(
    dsn="https://d5498a3385ed47bdb55caad8460138ab@o4508415306760192.ingest.de.sentry.io/4508415311741008",
)

engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine)
