from datetime import datetime
import pytest
from models.base import Base
from models.client import Client
from models.contract import Contract
from models.event import Event
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
def user_test_support(roles_setup, session):
    data = {
        "name": "support",
        "surname": "test",
        "email": "support@test.com",
        "password": hash_password("123456"),
        "role_id": "3",
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
        "sales_contact_id": user.id,
    }
    client = Client.create(session, **data)
    yield client, session


@pytest.fixture
def contract_test(client_test):
    client, session = client_test
    data = {
        "client_id": client.id,
        "total_contract_amount": "10000",
        "remaining_amount_to_pay": "10000",
    }
    contract = Contract.create(session, **data)
    yield contract, session


@pytest.fixture
def contract_test_signed(client_test):
    client, session = client_test
    data = {
        "client_id": client.id,
        "total_contract_amount": "10000",
        "remaining_amount_to_pay": "10000",
        "contract_signed_status": True,
    }
    contract = Contract.create(session, **data)
    yield contract, session


@pytest.fixture
def event_test(contract_test_signed):
    contract, session = contract_test_signed
    data = {
        "contract_id": contract.id,
        "name": "test",
        "location": "test location",
        "attendees": "200",
        "start_date": datetime(2000, 1, 1, 10, 00),
        "end_date": datetime(2000, 1, 1, 12, 00),
        "note": "",
    }
    event = Event.create(session, **data)
    yield event, session


@pytest.fixture
def valid_contract_for_event_setup(session):
    data = {
        "name": "sales1",
        "surname": "test",
        "email": "sales1@test.com",
        "password": hash_password("123456"),
        "role_id": "1",
    }
    user_sales_1 = User.create(session, **data)

    data = {
        "name": "sales2",
        "surname": "test",
        "email": "sales2@test.com",
        "password": hash_password("123456"),
        "role_id": "1",
    }
    user_sales_2 = User.create(session, **data)

    data = {
        "name": "test",
        "surname": "client",
        "email": "test1@client.com",
        "phone_number": "+33635624875",
        "company": "",
        "sales_contact_id": user_sales_1.id,
    }
    client_1 = Client.create(session, **data)

    data = {
        "name": "test",
        "surname": "client",
        "email": "test2@client.com",
        "phone_number": "+33635624875",
        "company": "",
        "sales_contact_id": user_sales_2.id,
    }
    client_2 = Client.create(session, **data)

    data = {
        "client_id": client_1.id,
        "total_contract_amount": "10000",
        "remaining_amount_to_pay": "10000",
    }
    contract_client_1_unsigned = Contract.create(session, **data)

    data = {
        "client_id": client_1.id,
        "total_contract_amount": "10000",
        "remaining_amount_to_pay": "10000",
        "contract_signed_status": True,
    }
    contract_client_1_signed = Contract.create(session, **data)

    data = {
        "client_id": client_2.id,
        "total_contract_amount": "10000",
        "remaining_amount_to_pay": "10000",
        "contract_signed_status": True,
    }
    contract_client_2_signed = Contract.create(session, **data)

    data = {
        "contract_id": contract_client_1_signed.id,
        "name": "test",
        "location": "test location",
        "attendees": "200",
        "start_date": datetime(2000, 1, 1, 10, 00),
        "end_date": datetime(2000, 1, 1, 12, 00),
        "note": "",
    }
    Event.create(session, **data)

    yield (
        user_sales_1,
        contract_client_1_signed,
        contract_client_1_unsigned,
        contract_client_2_signed,
        session,
    )
