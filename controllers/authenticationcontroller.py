from datetime import datetime, timedelta, UTC
from os import remove
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from getpass import getpass

from sqlalchemy import select

from models.user import User

SECRET_KEY = "This_is_the_secret_key"


class AuthenticationController:
    def __init__(self, view, session):
        self.view = view
        self.session = session

    def login(self):
        email, password = self.view.get_credentials()
        user = self.session.scalar(select(User).where(User.email == email))
        print(user)
        if not user:
            return self.view.get_login_error()

        ph = PasswordHasher()
        try:
            ph.verify(user.password, password)
        except VerifyMismatchError:
            return self.view.get_login_error()

        token = jwt.encode(
            {
                "user_id": user.id,
                "role": user.role.name,
                "exp": datetime.now(UTC) + timedelta(hours=1),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        with open("token.txt", "w") as token_file:
            token_file.write(token)

        self.view.login_successfull()

        return user

    def valid_token(self):
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
        try:
            with open("token.txt", "r") as token_file:
                return token_file.read()
        except FileNotFoundError:
            print("You are not logged in. Please, log in first.")
            return None

    @staticmethod
    def logout():
        try:
            remove("token.txt")
            print("Logged out successfully.")
        except FileNotFoundError:
            print("You are not logged in.")
