from io import StringIO
import pytest
from click.testing import CliRunner
import sys
from sqlalchemy import select
from models.user import User
from models.role import Role
from utils.validation import hash_password
from views import authenticationview
from commands.authentication import login, logout


class TestAuthentication:

    def test_login_success(self, mocker, test_sales_user):
        mocker.patch(
            "commands.authentication.authenticationview.get_credentials",
            return_value=["sales@test.com", "123456"],
        )

        runner = CliRunner()
        result = runner.invoke(login)

        # Assertions
        assert result.exit_code == 0
        assert "Login successfull" in result.output

    def test_login_unknow_email(self, mocker, test_sales_user):
        mocker.patch(
            "commands.authentication.authenticationview.get_credentials",
            return_value=["wrong.email@test.com", "123456"],
        )

        runner = CliRunner()
        result = runner.invoke(login)

        # Assertions
        assert result.exit_code != 0
        assert "This email do not have an account." in result.output

    def test_login_missmatch_email_password(self, mocker, test_sales_user):
        mocker.patch(
            "commands.authentication.authenticationview.get_credentials",
            return_value=["sales@test.com", "wrong_password"],
        )

        runner = CliRunner()
        result = runner.invoke(login)

        # Assertions
        assert result.exit_code != 0
        assert "Email and password do not match." in result.output
