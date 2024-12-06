import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from commands.user import user_delete
from models.base import Base
from models.user import User
from models.role import Role
from utils.validation import hash_password


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

@pytest.fixture
def setup_roles(session):
    roles = [
        Role(name="sales"),
        Role(name="management"),
        Role(name="support"),
    ]
    session.add_all(roles)
    session.commit()

@pytest.fixture
def test_sales_user(setup_roles, session):
    data = {
        "name": "sales",
        "surname": "test",
        "email": "sales@test.com",
        "password": hash_password("123456"),
        "role_id": "1",
    }

    user = User.create(session, **data)
    yield user
