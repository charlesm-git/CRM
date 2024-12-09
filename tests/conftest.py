from dotenv import load_dotenv
import pytest
import os
from models.base import Base
from models.client import Client
from models.user import User
from models.role import Role
from utils.validation import hash_password
from database import Session, engine


@pytest.fixture
def session():
    Base.metadata.create_all(engine)
    test_session = Session()
    yield test_session
    Base.metadata.drop_all(engine)
    test_session.close()


@pytest.fixture
def roles_setup(session):
    roles = [
        Role(name="sales"),
        Role(name="management"),
        Role(name="support"),
    ]
    session.add_all(roles)
    session.commit()


@pytest.fixture
def user_test_sales(roles_setup, session):
    data = {
        "name": "sales",
        "surname": "test",
        "email": "sales@test.com",
        "password": hash_password("123456"),
        "role_id": "1",
    }

    user = User.create(session, **data)
    yield user, session


@pytest.fixture
def user_test_management(roles_setup, session):
    data = {
        "name": "management",
        "surname": "test",
        "email": "management@test.com",
        "password": hash_password("123456"),
        "role_id": "2",
    }

    user = User.create(session, **data)
    yield user, session


@pytest.fixture
def client_test(user_test_sales):
    user, session = user_test_sales
    data = {
        "name": "test",
        "surname": "client",
        "email": "test@client.com",
        "phone_number": "+33635624875",
        "company": "",
        "sales_contact_id":user.id,
    }
    client = Client.create(session, **data)
    yield client, session
    
