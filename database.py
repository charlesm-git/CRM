import os
import sentry_sdk
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


is_test = os.getenv("TEST_ENV", "false").lower == "true"

# Load the appropriate .env file
if not is_test:
    load_dotenv()  # Load .env for normal app usage.

DATABASE_URL = os.getenv("DATABASE_URL")
SENTRY_DSN = os.getenv("SENTRY_DSN")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

sentry_sdk.init(dsn=SENTRY_DSN)

engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine)
