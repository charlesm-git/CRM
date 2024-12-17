from click.testing import CliRunner
from sqlalchemy import select
from commands.client import client_create, client_delete, client_update
from models.client import Client


class TestClientCommands:
    def test_client_create_success(self, mocker, user_test_sales):
        # Mock dependencies
        user, session = user_test_sales
        mock_valid_token = mocker.patch(
            "commands.client.valid_token", return_value={"user_id": user.id}
        )
        mock_has_permission = mocker.patch("commands.client.has_permission")
        mock_client_creation = mocker.patch(
            "commands.client.clientview.client_creation",
            return_value={
                "name": "test",
                "surname": "client",
                "email": "test@client.com",
                "phone_number": "+33635624875",
                "company": "",
            },
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(client_create)

        client = Client.get_by_id(session, 1)

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        mock_client_creation.assert_called_once()
        assert "Ressource created successfully" in result.output
        assert client.name == "test"
        assert client.email == "test@client.com"
        assert client.sales_contact_id == user.id

    def test_client_create_permission_error(self, mocker, client_test):
        # Mock dependencies
        mocker.patch("commands.client.valid_token")
        mocker.patch(
            "commands.client.has_permission",
            side_effect=PermissionError("Permission denied"),
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(client_create)

        # Assertions
        assert result.exit_code != 0
        assert "Permission denied" in result.output

    def test_client_create_integrity_error(self, mocker, client_test):
        # Mock dependencies
        user, session = client_test
        mocker.patch(
            "commands.client.valid_token", return_value={"user_id": user.id}
        )
        mocker.patch("commands.client.has_permission")
        mocker.patch(
            "commands.client.clientview.client_creation",
            return_value={
                "name": "test",
                "surname": "client",
                "email": "test@client.com",
                "phone_number": "+33635624875",
                "company": "",
            },
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(client_create)
        result = runner.invoke(client_create)

        # Assertions
        assert result.exit_code == 0
        assert (
            "A client with this email already exists. Check the database."
            in result.output
        )

    def test_client_update_success(self, mocker, client_test):
        # Mock dependencies
        client, session = client_test
        mock_valid_token = mocker.patch("commands.client.valid_token")
        mock_has_object_permission = mocker.patch(
            "commands.client.has_object_permission"
        )
        mock_user_update = mocker.patch(
            "commands.client.clientview.client_update",
            return_value={
                "name": "",
                "surname": "modified",
                "email": "",
                "phone_number": "",
                "company": "modified",
            },
        )
        mocker.patch(
            "commands.client.clientview.client_update_sales_contact",
            return_value="",
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(client_update, args=[str(client.id)])

        session.refresh(client)

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_object_permission.assert_called_once()
        mock_user_update.assert_called_once()
        assert "Ressource updated successfully" in result.output
        assert client.surname == "modified"
        assert client.company == "modified"

    def test_client_update_client_not_found(self, mocker, client_test):
        # Mock dependencies
        mock_valid_token = mocker.patch("commands.client.valid_token")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(client_update, args=["999"])

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        assert "Ressource not found" in result.output

    def test_client_update_sales_contact_input(
        self, mocker, client_test, user_test_management, user_test_sales
    ):
        # Mock dependencies
        client, session = client_test
        user_management = user_test_management[0]
        user_sales = user_test_sales[0]
        mock_valid_token = mocker.patch("commands.client.valid_token")
        mock_has_object_permission = mocker.patch(
            "commands.client.has_object_permission"
        )
        mock_user_update = mocker.patch(
            "commands.client.clientview.client_update"
        )

        # Side effect checks all the email possibilities
        mock_sales_contact_update = mocker.patch(
            "commands.client.clientview.client_update_sales_contact",
            side_effect=[
                "wrong@email.com",
                user_management.email,
                user_sales.email,
            ],
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(client_update, args=[str(client.id)])

        print(result.output)

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_object_permission.assert_called_once()
        mock_user_update.assert_called_once()
        assert mock_sales_contact_update.call_count == 3
        assert "Ressource not found" in result.output
        assert "This user is not part of the sales team." in result.output

    def test_client_delete_success(self, mocker, client_test):
        # Mock dependencies
        client, session = client_test
        mock_valid_token = mocker.patch("commands.client.valid_token")
        mock_has_permission = mocker.patch(
            "commands.client.has_object_permission"
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(client_delete, args=[str(client.id)])

        # Search for the deleted object in the database
        deleted_client = session.scalar(
            select(Client).where(Client.id == client.id)
        )

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        assert "Ressource deleted successfully" in result.output
        assert deleted_client is None

    def test_client_delete_client_not_found(self, mocker, client_test):
        # Mock dependencies
        mock_valid_token = mocker.patch("commands.client.valid_token")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(client_delete, args=["999"])

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        assert "Ressource not found" in result.output
