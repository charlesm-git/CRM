import pytest
from click.testing import CliRunner
from commands.user import user_create


# def test_user_create_success(mocker):
#     # Mock dependencies
#     mocker.patch("commands.user.valid_token", return_value="mock_token")
#     mocker.patch("commands.user.has_permission")
#     mock_user_creation = mocker.patch(
#         "views.userview.user_creation",
#         return_value={
#             "name": "Test",
#             "surname": "User",
#             "email": "test@example.com",
#             "password": "plain_password",
#             "role_id": "1",
#         },
#     )
#     mock_hash_password = mocker.patch(
#         "commands.user.hash_password", return_value="hashed_password"
#     )
#     mock_user_create = mocker.patch("models.user.User.create")
#     mock_is_created = mocker.patch("views.baseview.is_created")

#     # Run the Click command using CliRunner
#     runner = CliRunner()
#     result = runner.invoke(user_create)

#     # Assertions
#     assert result.exit_code == 0
#     mock_user_creation.assert_called_once()
#     mock_hash_password.assert_called_once_with("plain_password")
#     mock_user_create.assert_called_once_with(
#         mocker.ANY,
#         name="Test",
#         surname="User",
#         email="test@example.com",
#         password="hashed_password",
#         role_id="1",
#     )
#     mock_is_created.assert_called_once()


# def test_user_create_permission_error(mocker):
#     # Mock dependencies
#     mocker.patch("commands.user.valid_token", return_value="mock_token")
#     mocker.patch(
#         "commands.user.has_permission",
#         side_effect=PermissionError("Permission denied"),
#     )

#     runner = CliRunner()
#     result = runner.invoke(user_create)

#     # Assertions
#     assert result.exit_code != 0
#     assert "Permission denied" in result.output
