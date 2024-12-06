from datetime import datetime, timedelta, UTC
from os import remove
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import click
import jwt
from sqlalchemy import select
from dotenv import set_key, load_dotenv

from models.user import User
from database import Session
from views import authenticationview
from utils.validation import valid_token
from database import JWT_SECRET_KEY


@click.command(help="Login user")
def login():
    """
    CMR login Function using the user credentials.
    Creates a JWT.

    :return: returns a User instance matching the credentials or an error
    message
    """
    with Session() as session:
        # Get users credentials and look up un the database for an email match
        email, password = authenticationview.get_credentials()
        user = session.scalar(select(User).where(User.email == email))

        if not user:
            raise click.ClickException(authenticationview.get_email_error())

        # Check if the passwords match
        ph = PasswordHasher()
        try:
            ph.verify(user.password, password)
        except VerifyMismatchError:
            raise click.ClickException(authenticationview.get_mismatch_error())

        # Creates the JWT
        token = jwt.encode(
            {
                "user_id": user.id,
                "role": user.role.name,
                "exp": datetime.now(UTC) + timedelta(hours=1),
            },
            JWT_SECRET_KEY,
            algorithm="HS256",
        )
        
        # Store the JWT
        load_dotenv()
        set_key(".env", "JWT_TOKEN", token)

        authenticationview.login_successfull()


@click.command(help="Log out current user")
def logout():
    """Logout the user by deleting the JWT file"""
    with open(".env", "r+") as env_file:
        lines = env_file.readlines()

        lines = [line for line in lines if not line.startswith("JWT_TOKEN")]
        env_file.seek(0)
        env_file.writelines(lines)
        env_file.truncate()
    authenticationview.logout_successfull()


@click.command(help="Shows the current logged in user")
def current_user():
    with Session() as session:
        token = valid_token()
        user = User.get_by_id(session, token["user_id"])
        print(f"{user} in now connected.")
