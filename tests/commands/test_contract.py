import pytest
from click.testing import CliRunner
from sqlalchemy import select
from commands.contract import contract_create, contract_delete, contract_update
from models.contract import Contract


class TestContractCommands:
    def test_contract_create_success(self, mocker, client_test):
        # Mock dependencies
        client, session = client_test
        mock_valid_token = mocker.patch("commands.contract.valid_token")
        mock_has_permission = mocker.patch("commands.contract.has_permission")
        mock_client_id = mocker.patch(
            "commands.contract.contractview.get_client_id",
            return_value=client.id,
        )
        mock_contract_creation = mocker.patch(
            "commands.contract.contractview.contract_creation",
            return_value={
                "total_contract_amount": "10000",
                "remaining_amount_to_pay": "",
            },
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(contract_create)

        contract = Contract.get_by_id(session, 1)

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        mock_client_id.assert_called_once()
        mock_contract_creation.assert_called_once()
        assert "Ressource created successfully" in result.output
        assert contract.client_id == client.id
        assert contract.total_contract_amount == 10000
        assert contract.remaining_amount_to_pay == 10000
        assert contract.contract_signed_status is False

    def test_contract_create_permission_error(self, mocker, contract_test):
        # Mock dependencies
        mocker.patch("commands.contract.valid_token")
        mocker.patch(
            "commands.contract.has_permission",
            side_effect=PermissionError("Permission denied"),
        )
        
        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(contract_create)

        # Assertions
        assert result.exit_code != 0
        assert "Permission denied" in result.output

    def test_contract_update_success(self, mocker, contract_test):
        # Mock dependencies
        contract, session = contract_test
        mock_valid_token = mocker.patch("commands.contract.valid_token")
        mock_has_object_permission = mocker.patch(
            "commands.contract.has_object_permission"
        )
        mock_user_update = mocker.patch(
            "commands.contract.contractview.contract_update",
            return_value={
                "total_contract_amount": "5000",
                "remaining_amount_to_pay": "0",
                "contract_signed_status": "1",
            },
        )
        mocker.patch(
            "commands.contract.contractview.get_client_id",
            return_value="",
        )
        mocker.patch("commands.contract.capture_message")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(contract_update, args=[str(contract.id)])

        session.refresh(contract)

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_object_permission.assert_called_once()
        mock_user_update.assert_called_once()
        assert "Ressource updated successfully" in result.output
        assert contract.total_contract_amount == 5000
        assert contract.remaining_amount_to_pay == 0
        assert contract.contract_signed_status is True

    def test_contract_update_contract_not_found(self, mocker, contract_test):
        # Mock dependencies
        mock_valid_token = mocker.patch("commands.contract.valid_token")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(contract_update, args=["999"])

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        assert "Ressource not found" in result.output

    def test_contract_update_client_id_input(
        self, mocker, contract_test, user_test_management, user_test_sales
    ):
        # Mock dependencies
        contract, session = contract_test
        mocker.patch("commands.contract.valid_token")
        mocker.patch("commands.contract.has_object_permission")
        mocker.patch("commands.contract.contractview.contract_update")
        mocker.patch("commands.contract.capture_message")
        
        # Side effect check that wrong contract id input ("999")has the right 
        # behaviour
        mock_get_client_id = mocker.patch(
            "commands.contract.contractview.get_client_id",
            side_effect=["999", "1"],
        )
        
        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(contract_update, args=[str(contract.id)])

        print(result.output)

        # Assertions
        assert result.exit_code == 0
        assert mock_get_client_id.call_count == 2
        assert "Ressource not found" in result.output
        assert "Ressource updated successfully" in result.output

    def test_contract_delete_success(self, mocker, contract_test):
        # Mock dependencies
        contract, session = contract_test
        mock_valid_token = mocker.patch("commands.contract.valid_token")
        mock_has_permission = mocker.patch(
            "commands.contract.has_object_permission"
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(contract_delete, args=[str(contract.id)])

        # Search for the deleted object in the database
        deleted_contract = session.scalar(
            select(Contract).where(Contract.id == contract.id)
        )

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        assert "Ressource deleted successfully" in result.output
        assert deleted_contract is None

    def test_contract_delete_contract_not_found(self, mocker, contract_test):
        # Mock dependencies
        mock_valid_token = mocker.patch("commands.contract.valid_token")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(contract_delete, args=["999"])

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        assert "Ressource not found" in result.output
