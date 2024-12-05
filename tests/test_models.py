from datetime import datetime
from models.contract import Contract
from models.event import Event
from tests.conftest import session
from models.user import User
from models.client import Client


class TestModels:
    def test_user_model_manual_creation(self, session):
        test_user = User(
            name="user",
            surname="test",
            email="user@test.com",
            password="123456",
            role_id=1,
        )
        session.add(test_user)
        session.commit()
        session.refresh(test_user)

        # Assert
        assert test_user.id is not None
        assert test_user.name == "user"
        assert test_user.email == "user@test.com"

    def test_client_model_manual_creation(self, session):
        test_client = Client(
            name="client",
            surname="test",
            email="client@test.com",
            phone_number="+123456789",
            company="",
            sales_contact_id=1,
        )
        session.add(test_client)
        session.commit()
        session.refresh(test_client)

        # Assert
        assert test_client.id is not None
        assert test_client.name == "client"
        assert test_client.email == "client@test.com"

    def test_contract_model_manual_creation(self, session):
        test_contract = Contract(
            client_id=1,
            total_contract_amount=10000,
            remaining_amount_to_pay=10000,
        )
        session.add(test_contract)
        session.commit()
        session.refresh(test_contract)

        # Assert
        assert test_contract.id is not None
        assert test_contract.total_contract_amount == 10000
        assert test_contract.client_id == 1

    def test_event_model_manual_creation(self, session):
        test_event = Event(
            name="test",
            location="test location",
            attendees=50,
            start_date=datetime(2024, 1, 1, 10, 0),
            end_date=datetime(2024, 1, 1, 10, 0),
            contract_id=1,
        )
        session.add(test_event)
        session.commit()
        session.refresh(test_event)

        # Assert
        assert test_event.id is not None
        assert test_event.location == "test location"
        assert test_event.contract_id == 1
