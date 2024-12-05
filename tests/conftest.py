import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base


@pytest.fixture
def session():
    temp_db = "sqlite:///:memory:"
    engine = create_engine(temp_db)
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    test_session = TestSession()
    yield test_session
    test_session.close()
    engine.dispose()
