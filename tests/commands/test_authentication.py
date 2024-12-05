# import pytest
# from click.testing import CliRunner
# import jwt
# from sqlalchemy import select
# from models.user import User
# from models.role import Role
# from utils.validation import hash_password
# from views import authenticationview
# from commands.authentication import login, logout


# @pytest.fixture
# def setup_test_user(session):
#     test_role = Role(name="sales")
#     test_user = User(
#         name="user",
#         surname="test",
#         email="user@test.com",
#         password=hash_password("123456"),
#         role_id=1,
#     )
#     session.add(test_user)
#     session.commit()
#     yield test_user, test_role
#     session.delete(test_user)
#     session.commit()


# class TestAuthentication:
#     # Mock SECRET_KEY for JWT
#     SECRET_KEY = "test_secret"

#     def test_login_success(self, mocker, setup_test_user):
#         # Mock dependencies
#         mocker.patch(
#             "authenticationview.get_credentials",
#             return_value=["test@example.com", "test_password"],
#         )
#         mocker.patch("authenticationview.login_successfull")

#         # Mock database session
#         mock_session = mocker.patch("database.Session", autospec=True)
#         mock_session_instance = (
#             mock_session.return_value.__enter__.return_value
#         )

#         # Mock a User and Role instance
#         mock_user, mock_role = setup_test_user
#         mock_session_instance.scalar.return_value = mock_user

#         # Mock password verification
#         mock_ph = mocker.patch("argon2.PasswordHasher")
#         mock_ph_instance = mock_ph.return_value
#         mock_ph_instance.verify.return_value = True

#         # Mock JWT encoding
#         mock_jwt = mocker.patch("jwt.encode", return_value="fake_jwt_token")

#         runner = CliRunner()
#         result = runner.invoke(login)

#         # Assertions
#         assert result.exit_code == 0 # Ensure the command executes successfully
#         authenticationview.login_successfull.assert_called_once()
#         mock_jwt.assert_called_once_with(
#             {
#                 "user_id": mock_user.id,
#                 "role": mock_user.role.name,
#                 "exp": mocker.ANY,
#             },
#             self.SECRET_KEY,
#             algorithm="HS256",
#         )
#         mock_session_instance.scalar.assert_called_once_with(
#             select(User).where(User.email == "test@example.com")
#         )
