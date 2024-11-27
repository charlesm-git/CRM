import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

@pytest.fixture
def test_db():
    temp_db = "sqlite:///:memory:"
    engine = create_engine(temp_db)
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    yield session
    session.close()
    engine.dispose()
