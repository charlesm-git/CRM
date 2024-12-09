import pytest
import os
from click.testing import CliRunner
from sqlalchemy import select
from commands.user import user_create, user_delete, user_update
from commands.authentication import login
from database import DATABASE_URL
from models.user import User


def test_database_url_is_sqlite():
    assert DATABASE_URL == "sqlite:///:memory:"


def test_some_feature():
    is_test = os.getenv("TEST_ENV", "false")
    assert is_test == "true"


class TestUserCommands:
    def test_user_create_success(self, mocker, session, roles_setup):
        # Mock dependencies
        mock_valid_token = mocker.patch("commands.user.valid_token")
        mock_has_permission = mocker.patch("commands.user.has_permission")
        mock_user_creation = mocker.patch(
            "commands.user.userview.user_creation",
            return_value={
                "name": "creation",
                "surname": "user",
                "email": "test@user.com",
                "password": "password",
                "role_id": "1",
            },
        )
        mocker.patch("commands.user.capture_message")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(user_create)

        user = User.get_from_email(session, "test@user.com")

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        mock_user_creation.assert_called_once()
        assert "Ressource created successfully" in result.output
        assert user.name == "creation"
        assert user.role_id == 1

    def test_user_create_permission_error(self, mocker, session):
        # Mock dependencies
        mocker.patch("commands.user.valid_token")
        mocker.patch(
            "commands.user.has_permission",
            side_effect=PermissionError("Permission denied"),
        )

        runner = CliRunner()
        result = runner.invoke(user_create)

        # Assertions
        assert result.exit_code != 0
        assert "Permission denied" in result.output

    def test_user_create_integrity_error(self, mocker, session, roles_setup):
        # Mock dependencies
        mocker.patch("commands.user.valid_token")
        mocker.patch("commands.user.has_permission")
        mocker.patch(
            "commands.user.userview.user_creation",
            return_value={
                "name": "creation",
                "surname": "user",
                "email": "test@user.com",
                "password": "password",
                "role_id": "1",
            },
        )
        mocker.patch("commands.user.capture_message")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(user_create)
        result = runner.invoke(user_create)

        # Assertions
        assert result.exit_code != 0
        assert (
            "The email you provided is already used for another account. Try again."
            in result.output
        )

    def test_user_update_success(self, mocker, user_test_sales):
        # Mock dependencies
        user, session = user_test_sales
        mock_valid_token = mocker.patch("commands.user.valid_token")
        mock_has_permission = mocker.patch("commands.user.has_permission")
        mock_user_update = mocker.patch(
            "commands.user.userview.user_update",
            return_value={
                "name": "",
                "surname": "modified",
                "email": "",
                "password": "",
                "role_id": "3",
            },
        )
        mocker.patch("commands.user.capture_message")
        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(user_update, args=[user.email])

        session.refresh(user)

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        mock_user_update.assert_called_once()
        assert "Ressource updated successfully" in result.output
        assert user.surname == "modified"
        assert user.role_id == 3

    def test_user_update_user_not_found(
        self, mocker, session, user_test_sales
    ):
        # Mock dependencies
        mock_valid_token = mocker.patch("commands.user.valid_token")
        mock_has_permission = mocker.patch("commands.user.has_permission")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(user_update, args=["wrong.email@test.com"])

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        assert "Ressource not found" in result.output

    def test_user_delete_success(self, mocker, user_test_sales):
        # Mock dependencies
        user, session = user_test_sales
        mock_valid_token = mocker.patch("commands.user.valid_token")
        mock_has_permission = mocker.patch("commands.user.has_permission")
        mocker.patch("commands.user.capture_message")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(user_delete, args=[user.email])

        deleted_user = session.scalar(
            select(User).where(User.email == user.email)
        )

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        assert "Ressource deleted successfully" in result.output
        assert deleted_user is None

    def test_user_delete_user_not_found(self, mocker, user_test_sales):
        # Mock dependencies
        user, session = user_test_sales
        mock_valid_token = mocker.patch("commands.user.valid_token")
        mock_has_permission = mocker.patch("commands.user.has_permission")

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(user_delete, args=["wrong.email@test.com"])

        # Assertions
        assert result.exit_code == 0
        mock_valid_token.assert_called_once()
        mock_has_permission.assert_called_once()
        assert "Ressource not found" in result.output
