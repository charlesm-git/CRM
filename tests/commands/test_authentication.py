from click.testing import CliRunner
from commands.authentication import login


class TestAuthentication:
    def test_login_success(self, mocker, user_test_sales):
        mocker.patch(
            "commands.authentication.authenticationview.get_credentials",
            return_value=["sales@test.com", "123456"],
        )

        # Run the Click command using CliRunner
        runner = CliRunner()
        result = runner.invoke(login)

        # Assertions
        assert result.exit_code == 0
        assert "Login successfull" in result.output

    def test_login_unknow_email(self, mocker, user_test_sales):
        mocker.patch(
            "commands.authentication.authenticationview.get_credentials",
            return_value=["wrong.email@test.com", "123456"],
        )

        runner = CliRunner()
        result = runner.invoke(login)

        # Assertions
        assert result.exit_code != 0
        assert "This email do not have an account." in result.output

    def test_login_missmatch_email_password(self, mocker, user_test_sales):
        mocker.patch(
            "commands.authentication.authenticationview.get_credentials",
            return_value=["sales@test.com", "wrong_password"],
        )

        runner = CliRunner()
        result = runner.invoke(login)

        # Assertions
        assert result.exit_code != 0
        assert "Email and password do not match." in result.output
