from datetime import datetime, timedelta, UTC
from os import remove
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import click
import jwt

from sqlalchemy import select

from models.user import User
from database import Session
from views import authenticationview
from utils.validation import SECRET_KEY, valid_token


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
            SECRET_KEY,
            algorithm="HS256",
        )

        # Store the JWT
        with open("token.txt", "w") as token_file:
            token_file.write(token)

        authenticationview.login_successfull()


@click.command(help="Log out current user")
def logout():
    """Logout the user by deleting the JWT file"""
    try:
        remove("token.txt")
        print("Logged out successfully.")
    except FileNotFoundError:
        print("You are not logged in.")


@click.command(help="Shows the current logged in user")
def current_user():
    with Session() as session:
        token = valid_token()
        user = User.get_by_id(session, token["user_id"])
        print(f"{user} in now connected.")
