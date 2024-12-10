from datetime import datetime
import pytest
from click.testing import CliRunner
from sqlalchemy import select
from commands.event import (
    event_create,
    event_delete,
    event_update,
    event_update_support,
    valid_contract_selection,
)
from models.event import Event


class TestEventCommands:
    def test_event_create_success(
        self, mocker, contract_test_signed, user_test_sales
    ):
        # Mock dependencies
        contract, session = contract_test_signed
        user = user_test_sales[0]
        mock_valid_token = mocker.patch(
            "commands.event.valid_token", return_value={"user_id": user.id}
        )
        mock_has_permission = mocker.patch("commands.event.has_permission")
        mock_get_contract_id = mocker.patch(
            "commands.event.eventview.get_contract_id",
            return_value=contract.id,
        )
        mock_event_creation = mocker.patch(
            "commands.event.eventview.event_creation",
            return_value={
                "name": "test",
                "location": "test location",
                "attendees": "200",
                "start_date": datetime(2000, 1, 1, 10, 00),
                "end_date": datetime(2000, 1, 1, 12, 00),
                "note": "",
            },
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(event_create)
        print(result.output)

        event = Event.get_by_id(session, 1)

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        mock_get_contract_id.assert_called_once()
        mock_event_creation.assert_called_once()
        assert "Ressource created successfully" in result.output
        assert event.name == "test"
        assert event.attendees == 200
        assert event.note == ""

    def test_event_create_permission_error(self, mocker, contract_test):
        # Mock dependencies
        mocker.patch("commands.event.valid_token")
        mocker.patch(
            "commands.event.has_permission",
            side_effect=PermissionError("Permission denied"),
        )

        runner = CliRunner()
        result = runner.invoke(event_create)

        # Assertions
        assert result.exit_code != 0
        assert "Permission denied" in result.output

    def test_wrong_contract_id_selection(self, valid_contract_for_event_setup):
        # Call all the contract status possibilities
        (
            user,
            contract_already_used,
            contract_unsigned,
            contract_other_sales_user,
            session,
        ) = valid_contract_for_event_setup

        # Check the function with all the wrong contract selection 
        # possibilities
        token = {"user_id": user.id}
        contract_not_found = valid_contract_selection(token, session, "999")
        contract_other_sales_user = valid_contract_selection(
            token, session, contract_other_sales_user.id
        )
        contract_unsigned = valid_contract_selection(
            token, session, contract_unsigned.id
        )
        contract_already_used = valid_contract_selection(
            token, session, contract_already_used.id
        )

        # Assertions
        assert contract_not_found is False
        assert contract_other_sales_user is False
        assert contract_unsigned is False
        assert contract_already_used is False

    def test_event_update_success(self, mocker, event_test):
        # Mock dependencies
        event, session = event_test
        mock_valid_token = mocker.patch("commands.event.valid_token")
        mock_has_object_permission = mocker.patch(
            "commands.event.has_object_permission"
        )
        mock_event_update = mocker.patch(
            "commands.event.eventview.event_update",
            return_value={
                "name": "",
                "location": "modified",
                "attendees": "modified",
                "start_date": "",
                "end_date": "",
                "note": "modified",
            },
        )
        # First side effect checks that the function valid_contract_selection
        # is called. Second return no update on the contract id
        mocker.patch(
            "commands.event.eventview.get_contract_id", side_effect=["999", ""]
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(event_update, args=[str(event.id)])

        session.refresh(event)

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_object_permission.assert_called_once()
        mock_event_update.assert_called_once()
        assert "Ressource updated successfully" in result.output
        assert event.location == "modified"
        assert event.attendees == "modified"
        assert event.note == "modified"

    def test_event_update_event_not_found(self, mocker, event_test):
        # Mock dependencies
        mock_valid_token = mocker.patch("commands.event.valid_token")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(event_update, args=["999"])

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        assert "Ressource not found" in result.output

    def test_event_update_support_contact(
        self, mocker, event_test, user_test_support, user_test_sales
    ):
        # Mock dependencies
        event, session = event_test
        user_support = user_test_support[0]
        user_sales = user_test_sales[0]
        mock_valid_token = mocker.patch("commands.event.valid_token")
        mock_has_object_permission = mocker.patch(
            "commands.event.has_permission"
        )
        
        # Side effect checks all the email possibilities
        mock_support_contact_update = mocker.patch(
            "commands.event.eventview.get_support_contact_email",
            side_effect=[
                "wrong email format",
                "wrong@email.com",
                user_sales.email,
                user_support.email,
            ],
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(event_update_support, args=[str(event.id)])

        print(result.output)

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_object_permission.assert_called_once()
        assert mock_support_contact_update.call_count == 4
        assert "Ressource not found" in result.output
        assert "This user is not part of the support team." in result.output
        assert "Ressource updated successfully" in result.output

    def test_event_delete_success(self, mocker, event_test):
        # Mock dependencies
        event, session = event_test
        mock_valid_token = mocker.patch("commands.event.valid_token")
        mock_has_permission = mocker.patch(
            "commands.event.has_object_permission"
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(event_delete, args=[str(event.id)])

        # Search for the deleted object in the database
        deleted_event = session.scalar(
            select(Event).where(Event.id == event.id)
        )

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        assert "Ressource deleted successfully" in result.output
        assert deleted_event is None

    def test_event_delete_event_not_found(self, mocker, event_test):
        # Mock dependencies
        mock_valid_token = mocker.patch("commands.event.valid_token")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(event_delete, args=["999"])

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        assert "Ressource not found" in result.output
