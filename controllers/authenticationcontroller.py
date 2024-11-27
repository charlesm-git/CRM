from datetime import datetime, timedelta, UTC
from os import remove
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt

from sqlalchemy import select

from models.user import User

SECRET_KEY = "This_is_the_secret_key"


class AuthenticationController:
    def __init__(self, view, session):
        self.view = view
        self.session = session

    def login(self):
        """
        CMR login Function using the user credentials.
        Creates a JWT.

        :return: returns a User instance matching the credentials or an error
        message
        """
        # Get users credentials and look up un the database for an email match
        email, password = self.view.get_credentials()
        user = self.session.scalar(select(User).where(User.email == email))
        
        if not user:
            return self.view.get_email_error()

        # Check if the passwords match
        ph = PasswordHasher()
        try:
            ph.verify(user.password, password)
        except VerifyMismatchError:
            self.view.get_mismatch_error()
            return None

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

        self.view.login_successfull()

        return user

    def valid_token(self):
        """Check if the JWT is still valid"""
        token = self.load_token()

        if token is None:
            return False

        try:
            jwt.decode(token, SECRET_KEY, algorithms="HS256")
            return True
        except jwt.ExpiredSignatureError:
            print("Your session has expired. Please log in again")
        except jwt.InvalidTokenError:
            print("Invalid token. Please log in again")

    @staticmethod
    def load_token():
        """Load the JWT from the .twt file"""
        try:
            with open("token.txt", "r") as token_file:
                return token_file.read()
        except FileNotFoundError:
            print("You are not logged in. Please, log in first.")
            return None

    @staticmethod
    def logout():
        """Logout the user by deleting the JWT file"""
        try:
            remove("token.txt")
            print("Logged out successfully.")
        except FileNotFoundError:
            print("You are not logged in.")
